
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
var WORKFLOWDATA = {workflows:  {"1": 
                                    {"id":"1",
                                    "name": "Workflow 1",
                                    "variables": {"var1": "1, 2, z", "var2": "q"},
                                    "instances": 
                                        {"1": {"id": "1", 
                                        				"name": "Instance 1",
                                        				"Commands": {"Command 1": {}},
                                                        "BootDisk": "0",
                                                        "ReadDisks": [],
                                                        "WriteDisks": ["1"], 
                                                        "variables": {"var1": "1", "var2": "2"},
                                                        "machinetype": "n1-standard-1",
                                                        "location": "us-central1-a" 
                                                        }, 
                                         "2":{"id": "2", 
                                         				"name": "Instance 2",
                                         				"Commands": {"Command 2": {}},
                                                        "BootDisk": "0",
                                                        "ReadDisks": ["1"],
                                                        "WriteDisks": ["2"],
                                                        "variables": {"var1": "1-2", "var2": "2-2"},
                                                        "machinetype": "n1-standard-2",
                                                        "location": "us-central1-a" 
                                                        },
                                        },
                                    "disks": {"0": {"id": "0",
                                    					"name": "Disk 0",
                                    					"location":"us-central1-b", 
                                    					"disktype":"pd-standard", 
                                    					"size": "100",
                                    					"image": "1",
                                    					"variables": {"var1": "1, 2, z", "var2": "q"}
                                    					}, 
                                    		  "1": {"id": "1",
                                    		  			"name": "Disk 1",
                                    		  			"location":"us-central1-b", 
                                    					"disktype":"pd-standard", 
                                    					"size": "200",
                                    					"image": "2",
                                    					"variables": {"var1": "1, 2, z", "var2": "q"}
                                    					}, 
                                    		  "2": {"id":"2",
                                    		  			"name": "Disk 2",
                                    		  			"location":"us-central1-a", 
                                    					"disktype":"pd-standard", 
                                    					"size": "300",
                                    					"image": "1",
                                    					"variables": {"var1": "1, 2, z", "var2": "q"}
                                    					}
                                    		  }
                                }, "2":{
                                	"id": "2",
                                	"name": "Workflow 2",
                                	"variables": {"var1": "10, 2, az", "var2": "q2"},
                                    "instances": 
                                        {"3": {"id":"3", 
                                        				"name": "Instance 3",
                                        				"Commands": {"Command 3": {}},
                                                        "BootDisk": "3",
                                                        "ReadDisks": ["4"],
                                                        "WriteDisks": ["5"],
                                                        "variables": {"var1": "1-3", "var2": "1-4"},
                                                        "machinetype": "n1-standard-4",
                                                        "location": "us-central1-a" 
                                                        }, 
                                          "4":{"id": "4",
                                          				"name": "Instance 4",
                                          				"Commands": {"Command 4": {}},
                                                        "BootDisk": "6",
                                                        "ReadDisks": ["4"],
                                                        "WriteDisks": ["5", "3"],
                                                        "variables": {"var1": "1-5", "var2": "1-6"},
                                                        "machinetype": "n1-standard-16",
                                                        "location": "us-central1-a" 
                                                        }
                                    },
                                    "disks": {"3": {"id": "3",
                                    					"name": "Disk 3",
                                    					"location":"us-central1-a", 
                                    					"disktype":"pd-ssd", 
                                    					"size": "100",
                                    					"image": "1",
                                    					"variables": {"var1": "1, 2, z", "var2": "q"}
                                    					}, 
                                    		  "4": {"id": "4",
                                    		  			"name": "Disk 4",
                                    		  			"location":"us-central1-a", 
                                    					"disktype":"pd-standard", 
                                    					"size": "200",
                                    					"image": "2",
                                    					"variables": {"var1": "4", "var2": "q"}
                                    					}, 
                                    		  "5": {"id": "5",
                                    		  			"name": "Disk 5",
                                    		  			"location":"us-central1-a", 
                                    					"disktype":"pd-ssd", 
                                    					"size": "300",
                                    					"image": "1",
                                    					"variables": {"var1": "5", "var2": "q"}
                                    					}, 
                            			      "6": {"id": "6",
                            			      			"name": "Disk 6",
                            			      			"location":"us-central1-a", 
                                    					"disktype":"pd-standard", 
                                    					"size": "400",
                                    					"image": "2",
                                    					"variables": {"var1": "6", "var2": "q"}
                                    					}
                                    					}
                                    		  }
                                	},
                    images: {"1": {"id": "1", "name": "Image 1", "authaccount": "testauth@auth.com"}, 
                    		 "2":{"id": "2", "name": "Image 2", "authaccount": "testauth2@auth.com"},
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

function splitNameIntoIDAndName(name) {
	var split = name.split(": ");
	var id = split[0];
	var name = split.slice(1, split.length).join(": ");
	return({"id":id, "name":name});
}

// get a workflow
function getWorkflow(workflowSelect) {
	var workflows = getData(["workflows"]);
	// console.log(workflows);
    var currentWorkflowIDName = $("#"+workflowSelect+" :selected").html();
    // console.log(currentWorkflowIDName);
    var currentWorkflowID = splitNameIntoIDAndName(currentWorkflowIDName)["id"];
    // console.log(currentWorkflowID);
    // // var currentWorkflowName = splitNameIntoIDAndName(currentWorkflowIDName)["name"];
    // console.log(Object.keys(workflows));
    // console.log(typeof(Object.keys(workflows)[0]));
    // console.log(typeof(currentWorkflowID));
    // console.log(Object.keys(workflows)[0]+currentWorkflowID);
    // console.log(Object.keys(workflows)[0]==currentWorkflowID);
    // console.log($.inArray(currentWorkflowID, Object.keys(workflows))> -1);
    var currentWorkflow = workflows[currentWorkflowID];
    // console.log(currentWorkflow);
    return(currentWorkflow);
}

// get a variable in a workflow e.g. disk or instance
function getWorkflowVar(workflowSelect, varSelect, vartype) {
	var currentWorkflow = getWorkflow(workflowSelect);
	var varIDName = $("#"+varSelect+" :selected").html();
	console.log(varIDName);
    var varID = splitNameIntoIDAndName(varIDName)["id"];
    console.log(varID);
    console.log(Object.keys(currentWorkflow[vartype]));
    if (!($.inArray(varID, Object.keys(currentWorkflow[vartype]))>-1)) {return("None");}
    console.log(currentVar);
    console.log(currentWorkflow);
    console.log(currentWorkflow[vartype]);
    var currentVar = currentWorkflow[vartype][varID];
    console.log(currentVar);
    return(currentVar);
}

// get an instance
function getInstance(workflowSelect, instanceSelect) {
	return(getWorkflowVar(workflowSelect, instanceSelect, "instances"));
}

// get a disk
function getDisk(workflowSelect, diskSelect) {
	return(getWorkflowVar(workflowSelect, diskSelect, "disks"));
}

// get a disk by id
function getDiskByID(workflow, id) {
	console.log("disk by id");
	console.log(workflow["disks"][id]);
	return(workflow["disks"][id]);
}

// get a image by id
function getImageByID(id) {
	var data = getData(["images"]);
	return(data[id]);
}

// get an image
function getImage(imageSelect) {
	var images = getData(["images"]);
	var varIDName = $("#"+imageSelect+" :selected").html();
	console.log(varIDName);
	var varID = splitNameIntoIDAndName(varIDName)["id"];
	console.log(varID);
	console.log(Object.keys(images));
	if ($.inArray(varID, Object.keys(images))>-1) {
		return(images[varID]);
	} else {
		return("None");
	}
	
}

// get a command
function getCommand(workflowSelect, instanceSelect, commandSelect) {
	var instance = getInstance(workflowSelect, instanceSelect);
	var commandIDName = $("#"+commandSelect+" :selected").html();
	if (commandIDName == "New Command") {
		return("New Command");
	}
    var commandID = splitNameIntoIDAndName(commandIDName)["id"];
    var command = instance["commands"][commandID];
    return(command);
}

// standard naming scheme for options
function getOptions(vars, additionalOptions, selected) {
	var optionnames = [];
	$.each(vars, function(index, value) {
		optionnames.push(value["id"]+": "+value["name"]);
	});
	if (typeof additionalOptions === 'undefined') { additionalOptions = [];}
	optionnames = optionnames.concat(additionalOptions);
	// console.log(optionnames);
	// console.log("value");
	// console.log(value);
	if (typeof selected === 'undefined') { 
		selected = optionnames[0];
	} else {
		selected = selected["id"]+": "+selected["name"];
	}
	var result = "";
	for (i=0; i<optionnames.length; i++) {
		if (optionnames[i]==selected) {
			result = result + "<option selected>";
		} else {
			result = result + "<option>";
		}
		result += optionnames[i] + "</option>";
	}
	// console.log(result);
	return(result);
	// return("<option>"+optionnames.join("</option><option>")+"</option>");
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
    // var workflows = getData(["workflows"]);
    // // get current workflow name
    // var currentWorkflowName = $("#workflowVarWorkflowsSelect :selected").html();
    // console.log(currentWorkflowName);
    // get data for current workflow
    var currentWorkflow = getWorkflow("workflowVarWorkflowsSelect");
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
    $("#workflowVarWorkflowsSelect").html(getOptions(workflows));
    // "<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    updateWorkflowVarForm();
}

//// FUNCTIONS TO INITIALIZE AND UPDATE THE INSTANCE VARIABLES FORM

function updateInstanceVariablesInInstanceVarForm() {
    // var workflows = getData(["workflows"]); // get workflow data
    // var currentWorkflowName = $("#instanceVarWorkflowsSelect :selected").html(); // get current workflow name
    // var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    // var currentInstanceName = $("#instanceVarInstancesSelect :selected").html(); // get current instance name
    
    
    $("#instancevars").html(""); // clear out old variables
    var currentInstance = getInstance("instanceVarWorkflowsSelect", "instanceVarInstancesSelect");
    if (currentInstance!="None") {
	    console.log(currentInstance);
	    // currentWorkflow["instances"][currentInstanceName]; // get current instance
	    var instancevars = currentInstance["variables"]; // get current instance variables
	    var keys = Object.keys(instancevars); // get instance variable keys
	    // change key value pairs
	    for (i=0; i<keys.length; i++) {
	    	addInstancesVar(keys[i], instancevars[keys[i]]);
	    }
	}
}

// update instances select in instance variable form after workflow is selected
function updateInstancesInInstanceVarForm() {
    // var workflows = getData(["workflows"]); // get workflow data
    // var currentWorkflowName = $("#instanceVarWorkflowsSelect :selected").html(); // get current workflow name
    // var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    
    var currentWorkflow = getWorkflow("instanceVarWorkflowsSelect");
    // 
    // var options = Object.keys(currentWorkflow["instances"]).join("</option><option>");
    // console.log(options);
    // $("#instanceVarInstancesSelect").html("<option>"+options+"</option>");
	
	// update instance select html
	$("#instanceVarInstancesSelect").html(getOptions(currentWorkflow["instances"]));
	
	updateInstanceVariablesInInstanceVarForm();
}

// initialize the instance variable form
function initInstanceVarForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    // $("#instanceVarWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    $("#instanceVarWorkflowsSelect").html(getOptions(workflows));
    
    updateInstancesInInstanceVarForm();
}

//// FUNCTIONS FOR THE INSTANCE FORM

// add another read disk option to the instance
function addDisk(disk, type) {
    // get disk names
    // var workflows = getData(["workflows"]);
    // var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    // var currentWorkflow = workflows[currentWorkflowName];
    var currentWorkflow = getWorkflow("instanceWorkflowsSelect");
    if (disk!="") {
    	var orderedDiskNames = getOptions(currentWorkflow["disks"], ["None"], disk);	
    } else {
    	var orderedDiskNames = getOptions(currentWorkflow["disks"], ["None"]);
    }
    console.log("adding disk!");
    console.log(orderedDiskNames);
    
//     
    // diskNames;
    // if (diskname in diskNames) {
        // orderedDiskNames = [diskname, "None"]
    // } else {
        // orderedDiskNames = ["None"]
    // }
    // // get formatted disknames to add and mark the correct name as selected
    // for (i=0; i<diskNames.length; i++) {
        // if (diskNames[i]==diskname) {
            // orderedDiskNames.push("<option selected>"+diskNames[i]+"</option>");
        // } else {
            // orderedDiskNames.push("<option>"+diskNames[i]+"</option>");
        // }
    // }
    // add disknames to select
    if (type == "read") {
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceReadDisksSelect\">";
        var toadd = toadd + orderedDiskNames;
        var toadd = toadd + "</select>\n</div>\n<div class=\"form-group col-sm-4\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>\n</div></div>";
        $("#instanceReadDisks").append(toadd);    
    } else if (type == "readwrite") {
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceReadWriteDisksSelect\">";
        var toadd = toadd + orderedDiskNames;
        var toadd = toadd + "</select>\n</div>\n<div class=\"form-group col-sm-4\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>\n</div></div>";
        $("#instanceReadWriteDisks").append(toadd);
    } else if (type == "boot") {
        $("#instanceBootDisk").html("");
        var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceBootDiskSelect\">";
        var toadd = toadd + orderedDiskNames;
        var toadd = toadd + "</select>\n</div></div>";
        $("#instanceBootDisk").append(toadd);
    }   
}

// update the instance form once workflow is selected
function updateInstancesAndDisksOnInstanceForm() {
    // // get workflow data
    // var workflows = getData(["workflows"]);
    // // get current workflow name
    // var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    // // get data for current workflow
    // var currentWorkflow = workflows[currentWorkflowName];
    var currentWorkflow = getWorkflow("instanceWorkflowsSelect");
    // get instance and disk names
    var instanceOptions = getOptions(currentWorkflow["instances"], ["New Instance"]);
    var diskOptions =  getOptions(currentWorkflow["disks"], ["None"]);
    $("#instanceInstancesSelect").html(instanceOptions);
    $("#instanceBootDiskSelect").html(diskOptions);
    $("#instanceReadDisksSelect").html(diskOptions);
    $("#instanceReadWriteDisksSelect").html(diskOptions);
    
    updateInstanceOptionsOnInstanceForm();
}

// update disk options on instance form
function updateInstanceOptionsOnInstanceForm() {
    // // get workflow data
    // var workflows = getData(["workflows"]);
    // // get current workflow name
    // var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    // // get data for current workflow
    // var currentWorkflow = workflows[currentWorkflowName];
    // // get current instance name
    // var currentInstanceName = $("#instanceInstancesSelect :selected").html();
    
    var currentInstance = getInstance("instanceWorkflowsSelect", "instanceInstancesSelect");
    
    if (currentInstance != "None") {
        // get current instance
        // var currentInstance = currentWorkflow["instances"][currentInstanceName];
        
        // reset all disk option
        $("#instanceReadDisks").html("");    
        $("#instanceReadWriteDisks").html("");
        $("#instanceBootDisk").html("");
        
        // set instance name
        $("#instanceName").val(currentInstance["name"]);
        
        // add boot disk
        var workflow = getWorkflow("instanceWorkflowsSelect");
        addDisk(getDiskByID(workflow, currentInstance["BootDisk"]), "boot");
        // add read disks
        var readDiskNames = currentInstance["ReadDisks"];
        for (i=0; i<readDiskNames.length; i++) {
            addDisk(getDiskByID(workflow, readDiskNames[i]), "read");
        }
        // add read write disks
        var readWriteDiskNames = currentInstance["WriteDisks"];
        for (i=0; i<readWriteDiskNames.length; i++) {
            addDisk(getDiskByID(workflow, readWriteDiskNames[i]), "readwrite");
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
    $("#instanceWorkflowsSelect").html(getOptions(workflows));
    // $("#instanceWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    // update instance with instances specific to this workflow
    updateInstancesAndDisksOnInstanceForm();
    // update instance options with default first instance
    updateInstanceOptionsOnInstanceForm();
}

//// CODE FOR DISKS FORM

function updateDisksOnDiskForm() {
	// var workflows = getData(["workflows"]); // get workflow data
    // var currentWorkflowName = $("#instanceVarWorkflowsSelect :selected").html(); // get current workflow name
    // var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    var currentWorkflow = getWorkflow("diskWorkflowsSelect");
    console.log(currentWorkflow["disks"]);
    $("#diskDisksSelect").html(getOptions(currentWorkflow["disks"]));
    // // update instance select html
    // var options = Object.keys(currentWorkflow["disks"]).join("</option><option>");
    // console.log(options);
    // $("#diskDisksSelect").html("<option>"+options+"</option>");
	console.log("about to update disk options");
	updateDiskOptionsOnDiskForm();
	// "#diskWorkflowsSelect"
}

// this functions updates the disk form values when a disk is selected
function updateDiskOptionsOnDiskForm() {
	// // get workflow data
    // var workflows = getData(["workflows"]);
    // // get current workflow name
    // var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    // // get data for current workflow
    // var currentWorkflow = workflows[currentWorkflowName];
    // // get current instance name
    // var currentDiskName = $("#diskDisksSelect :selected").html();
    
    var currentDisk = getDisk("diskWorkflowsSelect", "diskDisksSelect");
    
    console.log(currentDisk);
    
    if (currentDisk != "None") {
        // // get current instance
        // var currentDisk = currentWorkflow["disks"][currentDiskName];
        // set name
        $("#diskName").val(currentDisk["name"]);
        // set size
        $("#diskSize").val(currentDisk["size"]);
        // set location
        setSelectorOption("diskLocationSelector", currentDisk["location"]);
        // set disk type
        setSelectorOption("diskTypeSelector", currentDisk["disktype"]);
        // set image
        var image = getImageByID(currentDisk["image"])
        setSelectorOption("diskImagesSelect", image["id"]+": "+image["name"]);
    }
}

// initialize the instance variable form
function initDiskForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    // $("#diskWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    $("#diskWorkflowsSelect").html(getOptions(workflows));
    updateDisksOnDiskForm();
    // get image data
    var images = getData(["images"]);
    // $("#diskImagesSelect").html("<option>"+Object.keys(images).join("</option><option>")+"</option>");
    $("#diskImagesSelect").html(getOptions(images));
    updateDisksInDiskVarForm();
}

// this function updates the disk names in the disk var form once a workflow is selected
function updateDisksInDiskVarForm() {
    // var workflows = getData(["workflows"]); // get workflow data
    // var currentWorkflowName = $("#diskVarWorkflowsSelect :selected").html(); // get current workflow name
    // var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    
    var currentWorkflow = getWorkflow("diskVarWorkflowsSelect");
    // update instance select html
    // Object.keys(currentWorkflow["disks"]).join("</option><option>");
    // $("#diskVarDisksSelect").html("<option>"+options+"</option>");
    $("#diskVarDisksSelect").html(getOptions(currentWorkflow["disks"]));
}

// this function updates the disk variables in the disk variable form once a disk is selected
function updateDiskVariablesInDiskVarForm() {
    // var workflows = getData(["workflows"]); // get workflow data
    // var currentWorkflowName = $("#instanceVarWorkflowsSelect :selected").html(); // get current workflow name
    // var currentWorkflow = workflows[currentWorkflowName]; // get data for current workflow
    // var currentDiskName = $("#diskVarDisksSelect :selected").html(); // get current disk name
    
    $("#diskvars").html(""); // clear out old variables
    var currentDisk = getDisk("instanceVarWorkflowsSelect", "diskVarDisksSelect");
    // var currentDisk = currentWorkflow["disks"][currentDiskName]; // get current disk
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
    $("#diskVarWorkflowsSelect").html(getOptions(workflows));
    // $("#diskVarWorkflowsSelect").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    updateDisksInDiskVarForm();
}

// update image form
function updateImageOptionsOnImageForm() {
	// get current image
    // var currentImageName = $("#imageImagesSelect :selected").html();
	
	var image = getImage("imageImagesSelect");
	console.log(image);
	// reset form vars
	$("#imageNameOnImageForm").val("");
    $("#authAccount").val("");
    // set form vars
    if (image !="None") {
    	// get image data
    	// var imagedata = getData(["images"]);
    	// var image = imagedata[currentImageName];
    	// console.log(image);
	    // set image name
	    $("#imageNameOnImageForm").val(image["name"]);
	    // set auth account
	    $("#authAccount").val(image["authaccount"]);
	}
}

// initialize images form
function initImageForm() {
    var images = getData(["images"]);
    $("#imageImagesSelect").html(getOptions(images, ["New Image"]));
    // $("#imageImagesSelect").html("<option>New Image</option><option>"+Object.keys(images).join("</option><option>")+"</option>");
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



// sets command attributes in command form
function setCommandAttributesInCommandForm() {
	// get command
    var command = getCommand("workflowInCommandForm", "instanceInCommandForm", "commandInCommandForm");
    // set command options
    if (command!= "New Command") {
	    var currentCommandID = splitNameIntoIDAndName(currentCommandIDName)["id"];
	    var currentCommandName = splitNameIntoIDAndName(currentCommandIDName)["name"];
	    var currentCommand = currentInstance["commands"][currentCommandID];
		// set command name
		$("#CommandName").val(currentCommand["name"]);
		// set command text
		$("#Command").val(currentCommand["command"]);
		// set command dependencies
		//var dependencies = currentCommand["dependencies"];	
		
    }
}

// sets command options in command form
function setCommandOptionsInCommandForm() {
    // // get current workflow
    // var currentWorkflowName = $("#workflowInCommandForm :selected").html();
    // var currentWorkflow = workflows[currentWorkflowName];
    // // get current instance
    // var currentInstanceName = $("#instanceInCommandForm :selected").html();
    // var currentInstance = currentWorkflow["instances"][currentInstanceName];
    var currentInstance = getInstance("workflowInCommandForm", "instanceInCommandForm");
    // set command options
    $("#instanceInCommandForm").html(getOptions(currentInstance["commands"], ["New Command"]));
    // $("#instanceInCommandForm").html("<option>New Command</option><option>"+Object.keys(currentInstance["commands"]).join("</option><option>")+"</option>");
    // set command attributes
    setCommandAttributesInCommandForm();
}

// sets Instance options in command form
function setInstanceOptionsInCommandForm() {
    // // get current workflow
    // var currentWorkflowName = $("#workflowInCommandForm :selected").html();
    // var currentWorkflow = workflows[currentWorkflowName];
    var currentWorkflow = getWorkflow("workflowInCommandForm");
    // set instance options
    $("#instanceInCommandForm").html(getOptions(currentWorkflow["instances"]));
    // $("#instanceInCommandForm").html("<option>"+Object.keys(currentWorkflow["instances"]).join("</option><option>")+"</option>");
	// set command options
	setCommandOptionsInCommandForm();
}

// initializes the command form
function initCommandForm() {
	var workflows = getData(["workflows"]);
	// set workflow options
	$("#workflowInCommandForm").html(getOptions(workflows));
	// $("#workflowInCommandForm").html("<option>"+Object.keys(workflows).join("</option><option>")+"</option>");
    setInstanceOptionsInCommandForm();
}

function addCommandDependency(command) {
	// // get disk names
    // var workflows = getData(["workflows"]);
    // var currentWorkflowName = $("#instanceWorkflowsSelect :selected").html();
    // var currentWorkflow = workflows[currentWorkflowName];
    
    var currentInstance = getInstance("workflowInCommandForm", "instanceInCommandForm");
    var commands = currentInstance["commands"];
    if (command != "") {
    	var options = getOptions(commands, ["None"], command);	
    } else {
    	var options = getOptions(commands, ["None"]);
    }

    // add disknames to select
    var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"commandDependenciesSelect\">";
    var toadd = toadd + options;
    var toadd = toadd + "</select>\n</div>\n<div class=\"form-group col-sm-4\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>\n</div></div>";
    $("#CommandDependencies").append(toadd);    
       
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


 