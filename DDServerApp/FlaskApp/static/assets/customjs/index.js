
//// GENERIC FUNCTIONS

// a function to set an option on a selector if available
function setSelectorOption(selectorID, optionToSelect) {
    // get all select elements
    var selects = $("#"+selectorID).children();
    // iterate over select elements and set selected any
    // element that shares the name of the optionToSelect
    // $(this) is the jquery object whereas select[i] is html dom
    selects.each(function(i) { 
        if ($( this ).html() == optionToSelect) {
            selects[i].setAttribute('selected', 'selected');
        }
    });
}

// removes the parent of a parent, for the delete buttons
function removeDivsDiv(e) {
    $(e).parent().parent().remove();
}

//// WORKFLOW DATA FUNCTIONS

// this object stores data about the current workflow, it should be updated
// whenever the user submits/saves/edits any of the workflow's data
var WORKFLOWDATA = {workflows:  {"Workflow 1": 
                                    {"variables": {"var1": "1, 2, z", "var2": "q"},
                                    "instances": 
                                        {"Instance 1": {"Commands": {"Command 1": {}},
                                                        "BootDisk": "Disk 0",
                                                        "ReadDisks": [],
                                                        "WriteDisks": ["Disk 1"], 
                                                        "variables": {"var1": "1", "var2": "2"},
                                                        "machinetype": "n1-standard-1",
                                                        "location": "us-central1-a" 
                                                        }, 
                                         "Instance 2":{"Commands": {"Command 2": {}},
                                                        "BootDisk": "Disk 0",
                                                        "ReadDisks": ["Disk 1"],
                                                        "WriteDisks": ["Disk 2"],
                                                        "variables": {"var1": "1-2", "var2": "2-2"},
                                                        "machinetype": "n1-standard-2",
                                                        "location": "us-central1-a" 
                                                        },
                                        },
                                    "disks": {"Disk 0": {"location":"us-central1-b", 
                                    					"disktype":"pd-standard", 
                                    					"size": "100",
                                    					"variables": {"var1": "1, 2, z", "var2": "q"}
                                    					}, 
                                    		  "Disk 1": {"location":"us-central1-b", 
                                    					"disktype":"pd-standard", 
                                    					"size": "200",
                                    					"variables": {"var1": "1, 2, z", "var2": "q"}
                                    					}, 
                                    		  "Disk 2": {"location":"us-central1-a", 
                                    					"disktype":"pd-standard", 
                                    					"size": "300",
                                    					"variables": {"var1": "1, 2, z", "var2": "q"}
                                    					}
                                    		  }
                                }, "Workflow 2":
                                    {"variables": {"var1": "10, 2, az", "var2": "q2"},
                                    "instances": 
                                        {"Instance 3": {"Commands": {"Command 3": {}},
                                                        "BootDisk": "Disk 3",
                                                        "ReadDisks": ["Disk 4"],
                                                        "WriteDisks": ["Disk 5"],
                                                        "variables": {"var1": "1-3", "var2": "1-4"},
                                                        "machinetype": "n1-standard-4",
                                                        "location": "us-central1-a" 
                                                        }, 
                                          "Instance 4":{"Commands": {"Command 4": {}},
                                                        "BootDisk": "Disk 6",
                                                        "ReadDisks": ["Disk 4"],
                                                        "WriteDisks": ["Disk 5", "Disk 3"],
                                                        "variables": {"var1": "1-5", "var2": "1-6"},
                                                        "machinetype": "n1-standard-16",
                                                        "location": "us-central1-a" 
                                                        }
                                    },
                                    "disks": {"Disk 3": {"location":"us-central1-a", 
                                    					"disktype":"pd-ssd", 
                                    					"size": "100",
                                    					"variables": {"var1": "1, 2, z", "var2": "q"}
                                    					}, 
                                    		  "Disk 4": {"location":"us-central1-a", 
                                    					"disktype":"pd-standard", 
                                    					"size": "200",
                                    					"variables": {"var1": "4", "var2": "q"}
                                    					}, 
                                    		  "Disk 5": {"location":"us-central1-a", 
                                    					"disktype":"pd-ssd", 
                                    					"size": "300",
                                    					"variables": {"var1": "5", "var2": "q"}
                                    					}, 
                            			      "Disk 6": {"location":"us-central1-a", 
                                    					"disktype":"pd-standard", 
                                    					"size": "400",
                                    					"variables": {"var1": "6", "var2": "q"}
                                    					}
                                    					}
                                    		  }
                                	},
                    images: {"Image 1": {"authaccount": "testauth@auth.com"}, 
                    		 "Image 2":{"authaccount": "testauth2@auth.com"},
                    		},
                    credentials: {"name": "testname", "serviceaccount": "test@test.com"},
                    }

// this function queries workflow data for a particular subset of the data
// keys is a list of keys to subset on in sequence
function getData(keys) {
    var result = WORKFLOWDATA;
    for (var i = 0; i < keys.length; i++) {
        result = result[keys[i]];
    }
    return(result);
}

// this function will make an ajax call to update the workflowdata variable
function updateWorkflowData() {
    return
}

//// SOME FUNCTIONS TO GET MACHINE TYPES

// machine type data in object
var ZONEMACHINETYPEDATA = {"us-east1-b": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "us-east1-c": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "europe-west1-d": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "asia-east1-b": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "asia-east1-c": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "us-east1-d": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "asia-east1-a": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "europe-west1-b": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-4", "n1-standard-8"], "us-central1-f": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "us-central1-c": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "us-central1-b": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"], "us-central1-a": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-4", "n1-standard-8"], "europe-west1-c": ["f1-micro", "g1-small", "n1-highcpu-16", "n1-highcpu-2", "n1-highcpu-32", "n1-highcpu-4", "n1-highcpu-8", "n1-highmem-16", "n1-highmem-2", "n1-highmem-32", "n1-highmem-4", "n1-highmem-8", "n1-standard-1", "n1-standard-16", "n1-standard-2", "n1-standard-32", "n1-standard-4", "n1-standard-8"]}

// gets machine types for a zone
function getMachineTypes(zone) {
    return(ZONEMACHINETYPEDATA[zone]);
}

// function to update machine types in a select element
function updateMachineTypes(elementID, zone) {
    var machineTypes = getMachineTypes(zone);
    console.log(machineTypes);
    var selecter =$("#"+elementID);
    console.log(selecter);
    selecter.html("");
    selecter.html("<option>"+machineTypes.join("</option><option>")+"</option>");
}

// update machine types based on zone for instances form
function updateInstanceFormMachineTypes() {
    var zone = $("#instanceLocationSelector :selected").html();
    updateMachineTypes("instanceMachineTypeSelector", zone);
}

//// SOME FUNCTIONS TO GET THE RIGHT VIEW FOR THE LEFT TOOLBAR BUTTONS

// this functions toggles the view between the tabs on the left hand side
function toggleView(section) {
    var ids = ["workflows_section", "instances_section", "disks_section", "commands_section", "images_section", "credentials_section"];
    for (var i = 0; i < ids.length; i++) {
        $('#'+ids[i]).hide();
    }
    $('#'+section).show();
}




//// OLD CRAP TO BE DELETED??

// // some functions for updating elements, not used yet!
// function updateElement(element_type, element_name, element_content) {
    // $(element_type+'[name='+element_name+']').html(element_content);
// }
//         
// function updateElements(updates) {
    // for (i=0; i<updates.length; i++) {
        // updateElement(updates[i].type, updates[i].name, updates[i].value);
    // }
// }
// 
// function updatePageElements(type, tid) {
    // var workflow_id =  
//     
    // $.get($SCRIPT_ROOT + '/_updatedata?tid='+tid+'&type='+type, {}, function(data, textStatus) {
        // console.log(data);
        // if (data["message"]!="") {
            // alert(data["message"]);             
        // }
        // updateElements(data["updates"]);
    // }, "json");
// }
// 
// // a function to submit a form via ajax, also not used yet
// function submitForm(section, callback) {
    // var formcontents = $('#'+section+'_form').children().find('input, select');
    // var tosubmit = {};
    // for (i=0; i<formcontents.length; i++) {
        // tosubmit[formcontents[i].name]=formcontents[i].value;               
    // }
    // console.log(tosubmit);
    // $.post($SCRIPT_ROOT + '/_addannotation?tid='+tid, tosubmit, function(data, textStatus) {
        // console.log(data);
        // alert(data["message"]);
        // callback();
        // return data;
    // }, "json");
// }
// 
// // workflow_editor
// function addEditorSection(section, testFormData) {
    // console.log("adding section "+section);
    // var myformwrapper = $("#"+section);
    // myformwrapper.append(testFormData); 
// }

//// SOME FUNCTIONS FOR ADDING AND REMOVING KEY VALUE INPUTS TO FORMS

// adds a key and value inputs plus a delete button
function addKeyValVariable(key, value, keyname, valuename, locationID) {
    var content = "";
    content = content + "\n<div class=\"row\">\n";
    content = content + "<div class=\"form-group col-sm-5\">\n";
    content = content + "<input type=\"text\" class=\"form-control\" name=\""+keyname+"\" placeholder=\"Variable Name (e.g. $JOBID)\"";
    if (key != "") {
    	content = content + " value=\""+key+"\""+">\n";	
    } else {
    	content = content + ">\n";
    }
    content = content + "</div>\n";
    content = content + "<div class=\"form-group col-sm-5\">\n";
    content = content + "<input type=\"text\" class=\"form-control\" name=\""+valuename+"\" placeholder=\"Variable Values Separated by Comma (e.g. 1, 2, 3)\" ";
    if (value != "") {
    	content = content + " value=\""+value+"\">\n"; 
    } else {
    	content = content + ">\n";
    }
    content = content + "</div>\n";
    content = content + "<div class=\"form-group col-sm-2\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>";
    content = content + "\n</div>\n</div>";
    $("#"+locationID).append(content); 	
}

// adds a variable to the workflow
function addWorkflowVar(key, value) {
    addKeyValVariable(key, value, "workflowvarname", "workflowvarvalue", "workflowvars");
} 

// adds a variable to the instance
function addInstancesVar(key, value) {
    addKeyValVariable(key, value, "instancevarname", "instancevarvalue", "instancevars");
}

// adds a variable to the disk
function addDisksVar(key, value) {
    addKeyValVariable(key, value, "diskvarname", "diskvarvalue", "diskvars");
}

//// FUNCTIONS TO INITIALIZE AND UPDATE THE WORKFLOW VARIABLES FORM

// updates the workflow variables form when a new workflow is selected
function updateWorkflowVarForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // get current workflow name
    var currentWorkflowName = $("#workflowVarWorkflowsSelect :selected").html();
    console.log(currentWorkflowName);
    // get data for current workflow
    var currentWorkflow = workflows[currentWorkflowName];
    console.log(currentWorkflow);
    // reset select
    $("#workflowvars").html("");
    // set variables of current workflow in form
    var variables = Object.keys(currentWorkflow["variables"]);
    for (i=0; i<variables.length; i++) {
        addWorkflowVar(variables[i], currentWorkflow["variables"][variables[i]])
    }
}

// initialize the workflow variable form
function initWorkflowVarForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#workflowVarWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    updateWorkflowVarForm();
}

//// FUNCTIONS TO INITIALIZE AND UPDATE THE INSTANCE VARIABLES FORM

function updateInstanceVariablesInInstanceVarForm() {
    var workflows = getData(["workflows"]); // get workflow data
    var currentWorkflowName = $("#instanceVarWorkflowsSelect :selected").html(); // get current workflow name
    var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    var currentInstanceName = $("#instanceVarInstancesSelect :selected").html(); // get current instance name
    $("#instancevars").html(""); // clear out old variables
    var currentInstance = currentWorkflow["instances"][currentInstanceName]; // get current instance
    var instancevars = currentInstance["variables"]; // get current instance variables
    var keys = Object.keys(instancevars); // get instance variable keys
    // change key value pairs
    for (i=0; i<keys.length; i++) {
    	addInstancesVar(keys[i], instancevars[keys[i]]);
    }
}

// update instances select in instance variable form after workflow is selected
function updateInstancesInInstanceVarForm() {
    var workflows = getData(["workflows"]); // get workflow data
    var currentWorkflowName = $("#instanceVarWorkflowsSelect :selected").html(); // get current workflow name
    var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    // update instance select html
    var options = Object.keys(currentWorkflow["instances"]).join("</option><option>");
    console.log(options);
    $("#instanceVarInstancesSelect").html("<option>"+options+"</option>");
	updateInstanceVariablesInInstanceVarForm();
}

// initialize the instance variable form
function initInstanceVarForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#instanceVarWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    updateInstancesInInstanceVarForm();
}

//// FUNCTIONS FOR THE INSTANCE FORM

// add another read disk option to the instance
function addDisk(diskname, type) {
    // get disk names
    var workflows = getData(["workflows"]);
    var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    var currentWorkflow = workflows[currentWorkflowName];
    var diskNames = Object.keys(currentWorkflow["disks"]);
    var orderedDiskNames = diskNames;
    if (diskname in diskNames) {
        orderedDiskNames = [diskname, "None"]
    } else {
        orderedDiskNames = ["None"]
    }
    // get formatted disknames to add and mark the correct name as selected
    for (i=0; i<diskNames.length; i++) {
        if (diskNames[i]==diskname) {
            orderedDiskNames.push("<option selected>"+diskNames[i]+"</option>");
        } else {
            orderedDiskNames.push("<option>"+diskNames[i]+"</option>");
        }
    }
    // add disknames to select
    if (type == "read") {
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceReadDisksSelect\">";
        var toadd = toadd + orderedDiskNames.join("");
        var toadd = toadd + "</select>\n</div>\n<div class=\"form-group col-sm-4\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>\n</div></div>";
        $("#instanceReadDisks").append(toadd);    
    } else if (type == "readwrite") {
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceReadWriteDisksSelect\">";
        var toadd = toadd + orderedDiskNames.join("");
        var toadd = toadd + "</select>\n</div>\n<div class=\"form-group col-sm-4\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>\n</div></div>";
        $("#instanceReadWriteDisks").append(toadd);
    } else if (type == "boot") {
        $("#instanceBootDisk").html("");
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceBootDiskSelect\">";
        var toadd = toadd + orderedDiskNames.join("");
        var toadd = toadd + "</select>\n</div></div>";
        $("#instanceBootDisk").append(toadd);
    }   
}

// update the instance form once workflow is selected
function updateInstancesAndDisksOnInstanceForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // get current workflow name
    var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    // get data for current workflow
    var currentWorkflow = workflows[currentWorkflowName];
    // get instance and disk names
    var instanceNames = ["New Instance"].concat(Object.keys(currentWorkflow["instances"]));
    var diskNames = ["None"].concat(Object.keys(currentWorkflow["disks"]));
    $("#instanceInstancesSelect").html("<option>"+instanceNames.join("</option><option>")+"</option>");
    $("#instanceBootDiskSelect").html("<option>"+diskNames.join("</option><option>")+"</option>");
    $("#instanceReadDisksSelect").html("<option>"+diskNames.join("</option><option>")+"</option>");
    $("#instanceReadWriteDisksSelect").html("<option>"+diskNames.join("</option><option>")+"</option>");
}

// update disk options on instance form
function updateInstanceOptionsOnInstanceForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // get current workflow name
    var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    // get data for current workflow
    var currentWorkflow = workflows[currentWorkflowName];
    // get current instance name
    var currentInstanceName = $("#instanceInstancesSelect :selected").html();
    
    if (currentInstanceName in currentWorkflow["instances"]) {
        // get current instance
        var currentInstance = currentWorkflow["instances"][currentInstanceName];
        
        // reset all disk option
        $("#instanceReadDisks").html("");    
        $("#instanceReadWriteDisks").html("");
        $("#instanceBootDisk").html("");
        
        // set instance name
        $("#instanceName").html(currentInstanceName);
        
        // add boot disk
        addDisk(currentInstance["BootDisk"], "boot");
        // add read disks
        var readDiskNames = currentInstance["ReadDisks"];
        for (i=0; i<readDiskNames.length; i++) {
            addDisk(readDiskNames[i], "read");
        }
        // add read write disks
        var readWriteDiskNames = currentInstance["WriteDisks"];
        for (i=0; i<readWriteDiskNames.length; i++) {
            addDisk(readWriteDiskNames[i], "readwrite");
        }
        
        // set location
        setSelectorOption("instanceLocationSelector", currentInstance["location"]);
        
        // set machine type
        setSelectorOption("instanceMachineTypeSelector", currentInstance["machinetype"]);
        
        
    } else {
        addDisk("", "boot");
    }
}

// initialize the instance form
function initInstanceForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#instanceWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    // update instance with instances specific to this workflow
    updateInstancesAndDisksOnInstanceForm();
    // update instance options with default first instance
    updateInstanceOptionsOnInstanceForm();
}

//// CODE FOR DISKS FORM

function updateDisksOnDiskForm() {
	var workflows = getData(["workflows"]); // get workflow data
    var currentWorkflowName = $("#instanceVarWorkflowsSelect :selected").html(); // get current workflow name
    var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    // update instance select html
    var options = Object.keys(currentWorkflow["disks"]).join("</option><option>");
    console.log(options);
    $("#diskDisksSelect").html("<option>"+options+"</option>");
	updateDiskOptionsOnDiskForm();
	// "#diskWorkflowsSelect"
}

// this functions updates the disk form values when a disk is selected
function updateDiskOptionsOnDiskForm() {
	// get workflow data
    var workflows = getData(["workflows"]);
    // get current workflow name
    var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    // get data for current workflow
    var currentWorkflow = workflows[currentWorkflowName];
    // get current instance name
    var currentDiskName = $("#diskDisksSelect :selected").html();
    
    if (currentDiskName in currentWorkflow["disks"]) {
        // get current instance
        var currentDisk = currentWorkflow["disks"][currentDiskName];
        // set name
        $("#diskName").val(currentDiskName);
        // set size
        $("#diskSize").val(currentDisk["size"]);
        // set location
        setSelectorOption("diskLocationSelector", currentDisk["location"]);
        // set disk type
        setSelectorOption("diskTypeSelector", currentDisk["disktype"]);
    }
}

// initialize the instance variable form
function initDiskForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#diskWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    updateDisksInDiskVarForm();
    // get image data
    var images = getData(["images"]);
    $("#diskImagesSelect").html("<option>"+Object.keys(images).join("</option><option>")+"</option>");
    updateDisksInDiskVarForm();
}

// this function updates the disk names in the disk var form once a workflow is selected
function updateDisksInDiskVarForm() {
    var workflows = getData(["workflows"]); // get workflow data
    var currentWorkflowName = $("#diskVarWorkflowsSelect :selected").html(); // get current workflow name
    var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    // update instance select html
    var options = Object.keys(currentWorkflow["disks"]).join("</option><option>");
    $("#diskVarDisksSelect").html("<option>"+options+"</option>");
}

// this function updates the disk variables in the disk variable form once a disk is selected
function updateDiskVariablesInDiskVarForm() {
    var workflows = getData(["workflows"]); // get workflow data
    var currentWorkflowName = $("#instanceVarWorkflowsSelect :selected").html(); // get current workflow name
    var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    var currentDiskName = $("#diskVarDisksSelect :selected").html(); // get current disk name
    $("#diskvars").html(""); // clear out old variables
    console.log(currentWorkflow["disks"]);
    console.log(currentDiskName);
    var currentDisk = currentWorkflow["disks"][currentDiskName]; // get current disk
    var diskvars = currentDisk["variables"]; // get current disk variables
    var keys = Object.keys(diskvars); // get disk variable keys
    // change key value pairs
    for (i=0; i<keys.length; i++) {
    	addDisksVar(keys[i], diskvars[keys[i]]);
    }
	// "#diskVarDisksSelect"
	// "diskvars"
}


// initialize the instance variable form
function initDiskVarForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#diskVarWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    updateDisksInDiskVarForm();
}

// update image form
function updateImageOptionsOnImageForm() {
	// get current image
    var currentImageName = $("#imageImagesSelect :selected").html();
	// reset form vars
	$("#imageNameOnImageForm").val("");
    $("#authAccount").val("");
    // set form vars
    if (currentImageName!="New Image") {
    	// get image data
    	var imagedata = getData(["images"]);
    	var image = imagedata[currentImageName];
    	console.log(image);
	    // set image name
	    $("#imageNameOnImageForm").val(currentImageName);
	    // set auth account
	    $("#authAccount").val(image["authaccount"]);
	}
}

// initialize images form
function initImageForm() {
    var images = getData(["images"]);
    $("#imageImagesSelect").html("<option>New Image</option><option>"+Object.keys(images).join("</option><option>")+"</option>");
	updateImageOptionsOnImageForm();
}

// init credentials form
function initCredentialsForm() {
	var credentials = getData(["credentials"]);
	// set name
	$("#credentialsName").val(credentials["name"]);
	// set account
	$("#serviceAccountEmail").val(credentials["serviceaccount"]);
}


//// CODE FOR COMMAND DEPENDENCIES

function splitNameIntoIDAndName(name) {
	var split = name.split(": ");
	var id = split[0];
	var name = split.slice(1, split.length).join(": ");
	return({"id":id, "name":name});
}

console.log(splitNameIntoIDAndName("id: hello"));

// sets command attributes in command form
function setCommandAttributesInCommandForm() {
	// get current workflow
    var currentWorkflowName = $("#workflowInCommandForm :selected").html();
    var currentWorkflow = workflows[currentWorkflowName];
    // get current instance
    var currentInstanceSelectedName = $("#instanceInCommandForm :selected").html();
    
    var currentInstanceName = splitNameIntoIDAndName(currentWorkflow["instances"][currentInstanceSelectedName])["name"];
    var currentInstanceID = splitNameIntoIDAndName(currentWorkflow["instances"][currentInstanceSelectedName])["id"];
    // get current command name
    var currentCommandName = $("#commandInCommandForm :selected").html();
    // set command options
    if (currentCommandName!= "New Command") {
    	var currentCommand = currentInstance["commands"][currentCommandName];
		// set command name
		$("#CommandName").val(currentCommandName);
		// set command text
		$("#Command").val(currentCommand["command"]);
		// set command dependencies
		var dependencies = currentCommand["dependencies"];
		
    }
    
}

// sets command options in command form
function setCommandOptionsInCommandForm() {
    // get current workflow
    var currentWorkflowName = $("#workflowInCommandForm :selected").html();
    var currentWorkflow = workflows[currentWorkflowName];
    // get current instance
    var currentInstanceName = $("#instanceInCommandForm :selected").html();
    var currentInstance = currentWorkflow["instances"][currentInstanceName];
    // set command options
    $("#instanceInCommandForm").html("<option>New Command</option><option>"+Object.keys(currentInstance["commands"]).join("</option><option>")+"</option>");
    // set command attributes
    setCommandAttributesInCommandForm();
}

// sets Instance options in command form
function setInstanceOptionsInCommandForm() {
    // get current workflow
    var currentWorkflowName = $("#workflowInCommandForm :selected").html();
    var currentWorkflow = workflows[currentWorkflowName];
    // set instance options
    $("#instanceInCommandForm").html("<option>"+Object.keys(currentWorkflow["instances"]).join("</option><option>")+"</option>");
	// set command options
	setCommandOptionsInCommandForm();
}

// initializes the command form
function initCommandForm() {
	var workflows = getData(["workflows"]);
	// set workflow options
	$("#workflowInCommandForm").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    setInstanceOptionsInCommandForm();
}

function addCommandDependency() {
	// get disk names
    var workflows = getData(["workflows"]);
    var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    var currentWorkflow = workflows[currentWorkflowName];
    var diskNames = Object.keys(currentWorkflow["disks"]);
    var orderedDiskNames = diskNames;
    if (diskname in diskNames) {
        orderedDiskNames = [diskname, "None"]
    } else {
        orderedDiskNames = ["None"]
    }
    // get formatted disknames to add and mark the correct name as selected
    for (i=0; i<diskNames.length; i++) {
        if (diskNames[i]==diskname) {
            orderedDiskNames.push("<option selected>"+diskNames[i]+"</option>");
        } else {
            orderedDiskNames.push("<option>"+diskNames[i]+"</option>");
        }
    }
    // add disknames to select
    if (type == "read") {
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceReadDisksSelect\">";
        var toadd = toadd + orderedDiskNames.join("");
        var toadd = toadd + "</select>\n</div>\n<div class=\"form-group col-sm-4\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>\n</div></div>";
        $("#instanceReadDisks").append(toadd);    
    } else if (type == "readwrite") {
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceReadWriteDisksSelect\">";
        var toadd = toadd + orderedDiskNames.join("");
        var toadd = toadd + "</select>\n</div>\n<div class=\"form-group col-sm-4\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>\n</div></div>";
        $("#instanceReadWriteDisks").append(toadd);
    } else if (type == "boot") {
        $("#instanceBootDisk").html("");
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceBootDiskSelect\">";
        var toadd = toadd + orderedDiskNames.join("");
        var toadd = toadd + "</select>\n</div></div>";
        $("#instanceBootDisk").append(toadd);
    }   
}


//// CODE TO RUN ON PAGE LOADING


$(document).ready(function(){
	// this code sets the write view on startup
    toggleView("disks_section");
    $(".nav li").on("click", function() {
        $(".nav li").removeClass("active");
        $(this).addClass("active");
    });

// start with at least one workflow var visible
    initWorkflowVarForm();
    initInstanceForm();
    initInstanceVarForm();
    initDiskVarForm();
    initDiskForm();
    initImageForm();
    initCredentialsForm();
});


 