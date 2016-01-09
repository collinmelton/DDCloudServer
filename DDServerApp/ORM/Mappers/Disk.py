'''
Created on Nov 20, 2015

@author: cmelton
'''

# imports
from DDServerApp.ORM import orm
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import sys, time

from DDServerApp.ORM import orm,Column,relationship,String,Integer, PickleType, Float,ForeignKey,backref,TextReader, joinedload_all
from DDServerApp.ORM import BASE_DIR, Boolean
#from DDServerApp.ORM.Mappers import GCEManagerBinding, LogFile

VERBOSE = True

class Disk(orm.Base):
    '''
    This class represents a disk to be generated on the Google Compute Engine.
    '''
    
    id = Column(Integer,primary_key=True)
    name = Column(String, index=True)
    location = Column(String)
    snapshot = Column(String)
#     image = Column(String)
    created = Column(Boolean)
    destroyed = Column(Boolean)
    mode = Column(String)
    formatted = Column(Boolean)
    disk_type = Column(String)
    init_source = Column(String)
    shutdown_dest = Column(String)
    image_id = Column(Integer, ForeignKey("image.id"))
    image = relationship("Image", backref = "disks")
    gce_manager_id = Column(Integer, ForeignKey("gcemanagerbinding.id"))
    gce_manager = relationship("GCEManagerBinding", backref = "disks")
    log_id = Column(Integer, ForeignKey("logfile.id"))
    log = relationship("LogFile", backref = "disks")
    size = Column(Integer)

    def __init__(self, name, size, location, snapshot=None, image=None, disk_type = 'pd-standard', 
                 init_source="", shutdown_dest="", gce_manager=None, log = None):
        self.name=name
        self.size=size
        self.location=location
        self.snapshot=snapshot
        self.image=image
        self.created=False
        self.destroyed=False
        self.disk=None
        self.mode="READ_WRITE"
        self.printToLog("initialized disk class")
        self.formatted=False
        self.disk_type=disk_type
        self.init_source = init_source
        self.shutdown_dest = shutdown_dest
        self.gce_manager = gce_manager
        self.log = log

    # adds myDriver, disk, and log to instance
    def reinit(self, myDriver, log):
#         self.gce_manager = myDriver
#         self.log = log
        # if already created and not destroyed update the disk to see if it is still present on gce
        if self.created and not self.destroyed: self.updateDisk()

    # string output
    def __str__(self):
        return self.name
    
    # representation output
    def __repr__(self):
        return self.name

    # removes content that should not be on the disk (i.e. content saved to disk if a prior instance was shutdown prior to completing)
    def contentRestore(self, restoreProgramPath):
        return restoreProgramPath+ " --P /mnt/"+self.name +" --F /mnt/"+self.name+"/"+"disk.content"

    # saves the directories and files stored on the disk 
    def contentSave(self, saveProgramPath):
        return saveProgramPath+ " --P /mnt/"+self.name +" --F /mnt/"+self.name+"/"+"disk.content"

    # returns a script to initialize drive from some source (i.e. another disk or from a storage bucket)
    def initialization_script(self):
        if self.init_source != "":
            return "gsutil rsync -r "+self.init_source+" /mnt/"+self.name
        return ""
    
    # returns a script to save disk contents to dest directory   
    def shutdown_save_script(self):
        if self.shutdown_dest != "":
            return "gsutil rsync -r /mnt/"+self.name+" "+self.shutdown_dest
        return ""

    # returns a script for mounting the disk  
    def mount_script(self, isWrite):
        result="mkdir -p /mnt/"+self.name
        if self.formatted:
            if isWrite:
                result+="\nmount /dev/disk/by-id/google-"+self.name+" /mnt/"+self.name+" -t ext4"
            else:
                result+="\nmount -o ro,noload /dev/disk/by-id/google-"+self.name+" /mnt/"+self.name+" -t ext4"
        else:
            result+="\n/usr/share/google/safe_format_and_mount -m 'mkfs.ext4 -F' /dev/disk/by-id/google-"+self.name+" /mnt/"+self.name
        self.formatted=True
        return result
    
    # returns s script to unmount disk
    def unmount_script(self):
        result = "umount /mnt/"+self.name
        return result 
    
    # set disk attribute based on name
    def setDisk(self, disks):
        for disk in disks:
            if disk.name==self.name:
                self.disk=disk
                self.created=True
                self.formatted=True
    
    # print to log file
    def printToLog(self, text):
        if "log" in self.__dict__ and self.log!=None:
            output=self.name+"\t"+text
            self.log.write(output)

    # some function to output class data in tsv form
    def toString(self):
        tabDelim=self.tabDelimSummary()
        return("\n".join([tabDelim["header"],tabDelim["values"]]))

    # method to create disk on GCE
    def create(self):
        self.printToLog("trying to create disk... destroyed: "+str(self.destroyed)+" created: "+str(self.created)+" None: "+str(self.disk==None))
        if self.destroyed or not self.created:
            if self.image == None: imagename = None
            else: imagename = self.image.name 
            disk=self.trycommand(self.gce_manager.create_volume, self.size, self.name, location=self.location, snapshot=self.snapshot, image=imagename, ex_disk_type=self.disk_type)
            self.created=True
            self.destroyed=False
            self.printToLog("created disk on GCE")
        else:
            self.printToLog("did not create disk on GCE")
            disk = None
        self.disk = disk
        return disk
    
    # method to update disk with current disk on GCE
    def updateDisk(self):
        self.printToLog("updating disk "+self.name)
        if (self.created): # and ("disk" not in self.__dict__ or self.disk ==None): 
            disk=self.trycommand(self.gce_manager.ex_get_volume, self.name)
            if VERBOSE: print "updated disk", disk
        else: disk = None
        self.disk = disk
        return disk
    
    # destroy disk on GCE
    def destroy(self):
        disk = self.updateDisk()
        if VERBOSE: print "created", self.created, "destroyed", self.destroyed
        if self.created and not self.destroyed: 
            self.trycommand(self.gce_manager.destroy_volume, disk)
            self.printToLog("destroyed disk on GCE")
        self.destroyed=True
        self.disk = None

    # destroy disk only if its not needed for future instances
    def destroyifnotneeded(self, instances):
        if instances!=None:
            # for each instance look to see if the disk is needed, if it is needed and the instance is not complete don't destroy (ie return)
            for instance_name in instances:
                inst = instances[instance_name]
                disk_names=map(lambda x: x.name, inst.read_disks+inst.read_write_disks)
                if self.name in disk_names:
                    if instances[instance_name].status!="complete":
                        return
            if VERBOSE: print "should destroy "+self.name
            self.destroy()

    # attach disk to instance
    def attach(self, instance):
        self.printToLog("attached disk to "+instance.name+" on GCE")
        disk = self.updateDisk()
        node = instance.updateNode()
        if instance.node!=None:
            self.trycommand(disk.attach, node)
    
    # detach disk from instance
    def detach(self, inst):
        if self.created and not self.destroyed:
            disk = self.updateDisk()
            node = inst.updateNode()
            self.printToLog("trying to detach disk on GCE from "+inst.name)
            self.trycommand(self.gce_manager.detach_volume, disk, node)
            self.printToLog("detached disk on GCE from "+inst.name)

    # try command for certain number of tries, sometimes GCE API doesn't work the first time its called
    def trycommand(self, func, *args, **kwargs):
        retries = 3
        tries = 0
        while tries<retries:
            try:
                x = func(*args, **kwargs)
                return x
            except:
                e = sys.exc_info()[0]
                tries +=1
                time.sleep(10)
                self.printToLog(str(func) + " Error: "+str(e)+ " try #"+str(tries)) 
        return None
    
    @staticmethod
    def findByName(session, name, user):
        from DDServerApp.ORM.Mappers.Workflow import Workflow, DiskWorkflowLink
        dids=session.query(Disk).join(DiskWorkflowLink).join(Workflow).filter(Disk.name==name).filter(Workflow.user_id==user.id).all()
        if len(dids)==0: return None
        else: return dids[0]  