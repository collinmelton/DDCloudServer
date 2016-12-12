# DDCloudServer
This software is designed to run genomics workflows on the Google Compute Engine. The distinguishing characteristic of this software is that it is designed to automatically mount and unmount disk storage as needed during the course of the workflow. This is in contrast to NFS storage or saving intermediate results to cloud storage. In certain use cases this strategy better optimizes resource utilization.

# Contents
- [Get Setup with GCE](#get-setup-with-gce)
- [Configure GCE Image](#configure-gce-image)
- [Get Service Account Authentication Info](#get-service-account-authentication-info) 
- [Using the Webserver](#using-the-webserver)
- [Alternative Licensing](#alternative-licensing)

# Get Setup with GCE
Get a GCE Account and setup a Google Cloud Storage bucket. URI should look something like this gs://bucketname/

# Configure GCE Image
In this section we will configure a GCE Image for use as the OS on both the Master and Worker instances. 

## Boot GCE Instance

From the GCE developers console boot a new instance. I've chosen CENTOS6.6 as the base image, but if you use a different base you may need to modify the software installation below. Make sure to enable full access to storage during setup. This is important because you will save you image to your Google Cloud Storage bucket. 

## Install Software (for CENTOS6.6)

1. SSH into the new instance. 

2. Install Git

	sudo yum install git
	
3. Clone this project and note project location

	git clone https://github.com/collinmelton/DDCloudServer.git

4. Note the current path. This is needed later when specifying your image in a workflow.
    
    pwd -P
	
4. Install project specific dependencies

    bash DDCloudServer/Setup/TestWorkerSetup.sh

## Create Image and Save to Cloud Storage

    Follow instructions here: https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images

    You need to delete your instance but keep the boot disk around. You can then create an image from that boot disk using the web console.


# Get Service Account Authentication Info
In order to run the software you need to get a service account email address and a pem file. See instructions here: https://cloud.google.com/storage/docs/authentication#service_accounts

You should make a pem file and note your service account email address in the format: numbersandletters@developer.gserviceaccount.com

## Example for instance name test1 with boot disk named boot1.

gcloud compute --project "cloudtest-152304" instances set-disk-auto-delete test1 --no-auto-delete --disk boot1 --zone "us-central1-a"

gcloud compute --project "cloudtest-152304" instances delete test1 --zone "us-central1-a"

gcloud compute --project "cloudtest-152304" images create workertest --source-disk boot1 --source-disk-zone "us-central1-a" --family worker

# Launch Webserver

Launch a new GCE instance on Centos6.6 with the following startup script. Make sure to enable https. You should specify the following as the startup script when launching the server.

## Install gcloud.

    https://cloud.google.com/sdk/

## Clone the project repository.

	git clone https://github.com/collinmelton/DDCloudServer.git

## Start your server (replace project with the name of your own project).

    gcloud compute --project "cloudtest-152304" instances create "ddserver2" --zone "us-central1-c" --machine-type "n1-standard-1" --subnet "default" --maintenance-policy "MIGRATE" --scopes default="https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --tags "https-server" --image "/centos-cloud/centos-6-v20161208" --boot-disk-size "10" --boot-disk-type "pd-standard" --boot-disk-device-name "ddserver2" --metadata-from-file startup-script=DDCloudServer/Setup/ServerSetup.sh

    gcloud compute --project "cloudtest-152304" firewall-rules create "default-allow-https" --allow tcp:443 --network "default" --source-ranges "0.0.0.0/0" --target-tags "https-server"

Please allow a few minutes for the server to install and launch.


# Using the Webserver
First navigate your webbrowser to the public ip address of the webserver using https so https://your-servers-ip-address/. 

## Sign In or login
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Login_login.png "Login")

## Setup a New Workflow
Setting up a new workflow requires some general details which include specifying your GCE credentials and adding an image. Next you should first specify disks that will be used by the instances, then instances that use the disks, and finally commands to be run on each instance. Some screenshots showing these steps are included below:

### Name Your Workflow and Describe Workflow Variables
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_workflows.png "New Workflow")

### Add Your Credentials
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_credentials.png "Add Credentials")

### Add an Image
Make sure to fill in Installation Directory. If you neglect this step or specify the path incorrectly the worker instances won't be able to communicate with your server.
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_images.png "Add Image")

### Specify Disks
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_disks.png "Add Disks")

### Specify Instances
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_instances.png "Add Instances")

### Specify Commands
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Setup_commands.png "Add Commands")
	
## Launch Your Workflow
A new workflow can't be launched if an existing workflow with the same type is already running. To relaunch stop the first one and refresh until you can start a new workflow. The user experience here is not ideal yet (: Furthermore, there are currently no safeguards against launching mispecified workflows. 
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Launcher.png "Launch Workflow")

## View Results and Monitor Performance
The dashboard is divided into the following sections: (1) select a workflow, (2) view the instances in a workflow, (3) view commands in an instance, and (4) finally view performance of a command. Screenshots depicting these sections are provide below:

### Select a Workflow and Instance
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Dashboard_instances.png "Select Workflow and Instance")

### Select an Instance
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Dashboard_commands.png "Select Command")

### Select an Instance
![alt text](https://github.com/collinmelton/DDCloudServer/blob/master/InstructiveImages/Dashboard_performance.png "View Performance")

# Alternative Licensing
This project is licensed open source under GNU GPLv2. To inquire about alternative licensing options please contact the Stanford Office of Technology Licensing (www.otl.stanford.edu).
