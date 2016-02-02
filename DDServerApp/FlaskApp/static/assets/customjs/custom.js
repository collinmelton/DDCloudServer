
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
var WORKFLOWDATA = {};
					// {workflows:  {"1": 
                                    // {"id":"1",
                                    // "name": "Workflow 1",
                                    // "variables": {"var1": "1, 2, z", "var2": "q"},
                                    // "instances": 
                                        // {"1": {"id": "1", 
                                        				// "name": "Instance 1",
                                        				// "Commands": {"1": {"id":"1", "name":"1", "command":"do a", "dependencies":[]},
                                        							// "2": {"id":"2", "name":"1", "command":"do b", "dependencies":["1"]},
                                        							// "3": {"id":"3", "name":"1", "command":"do c", "dependencies":["1"]},
                                        							// "4": {"id":"4", "name":"1", "command":"do d", "dependencies":["2", "3"]},
                                        							// },
                                                        // "BootDisk": "0",
                                                        // "ReadDisks": [],
                                                        // "WriteDisks": ["1"], 
                                                        // "variables": {"var1": "1", "var2": "2"},
                                                        // "machinetype": "n1-standard-1",
                                                        // "location": "us-central1-a",
                                                        // "dependencies":[], 
                                                        // }, 
                                         // "2":{"id": "2", 
                                         				// "name": "Instance 2",
                                         				// "Commands": {"1": {"id":"1", "name":"1", "command":"do a", "dependencies":[]},
                                        							// "2": {"id":"2", "name":"1", "command":"do b", "dependencies":["1"]},
                                        							// "3": {"id":"3", "name":"1", "command":"do c", "dependencies":["1"]},
                                        							// "4": {"id":"4", "name":"1", "command":"do d", "dependencies":["2", "3"]},
                                        							// },
                                                        // "BootDisk": "0",
                                                        // "ReadDisks": ["1"],
                                                        // "WriteDisks": ["2"],
                                                        // "variables": {"var1": "1-2", "var2": "2-2"},
                                                        // "machinetype": "n1-standard-2",
                                                        // "location": "us-central1-a",
                                                        // "dependencies":["1"], 
                                                        // },
                                        // },
                                    // "disks": {"0": {"id": "0",
                                    					// "name": "Disk 0",
                                    					// "location":"us-central1-b", 
                                    					// "disktype":"pd-standard", 
                                    					// "size": "100",
                                    					// "image": "1",
                                    					// "variables": {"var1": "1, 2, z", "var2": "q"}
                                    					// }, 
                                    		  // "1": {"id": "1",
                                    		  			// "name": "Disk 1",
                                    		  			// "location":"us-central1-b", 
                                    					// "disktype":"pd-standard", 
                                    					// "size": "200",
                                    					// "image": "2",
                                    					// "variables": {"var1": "1, 2, z", "var2": "q"}
                                    					// }, 
                                    		  // "2": {"id":"2",
                                    		  			// "name": "Disk 2",
                                    		  			// "location":"us-central1-a", 
                                    					// "disktype":"pd-standard", 
                                    					// "size": "300",
                                    					// "image": "1",
                                    					// "variables": {"var1": "1, 2, z", "var2": "q"}
                                    					// }
                                    		  // }
                                // }, "2":{
                                	// "id": "2",
                                	// "name": "Workflow 2",
                                	// "variables": {"var1": "10, 2, az", "var2": "q2"},
                                    // "instances": 
                                        // {"3": {"id":"3", 
                                        				// "name": "Instance 3",
                                        				// "Commands": {"1": {"id":"1", "name":"1", "command":"do a", "dependencies":[]},
                                        							// "2": {"id":"2", "name":"1", "command":"do b", "dependencies":["1"]},
                                        							// "3": {"id":"3", "name":"1", "command":"do c", "dependencies":["1"]},
                                        							// "4": {"id":"4", "name":"1", "command":"do d", "dependencies":["2", "3"]},
                                        							// },
                                                        // "BootDisk": "3",
                                                        // "ReadDisks": ["4"],
                                                        // "WriteDisks": ["5"],
                                                        // "variables": {"var1": "1-3", "var2": "1-4"},
                                                        // "machinetype": "n1-standard-4",
                                                        // "location": "us-central1-a",
                                                        // "dependencies":[], 
                                                        // }, 
                                          // "4":{"id": "4",
                                          				// "name": "Instance 4",
                                          				// "Commands": {"1": {"id":"1", "name":"1", "command":"do a", "dependencies":[]},
                                        							// "2": {"id":"2", "name":"1", "command":"do b", "dependencies":["1"]},
                                        							// "3": {"id":"3", "name":"1", "command":"do c", "dependencies":["1"]},
                                        							// "4": {"id":"4", "name":"1", "command":"do d", "dependencies":["2", "3"]},
                                        							// },
                                                        // "BootDisk": "6",
                                                        // "ReadDisks": ["4"],
                                                        // "WriteDisks": ["5", "3"],
                                                        // "variables": {"var1": "1-5", "var2": "1-6"},
                                                        // "machinetype": "n1-standard-16",
                                                        // "location": "us-central1-a",
                                                        // "dependencies":["1", "1"], 
                                                        // }
                                    // },
                                    // "disks": {"3": {"id": "3",
                                    					// "name": "Disk 3",
                                    					// "location":"us-central1-a", 
                                    					// "disktype":"pd-ssd", 
                                    					// "size": "100",
                                    					// "image": "1",
                                    					// "variables": {"var1": "1, 2, z", "var2": "q"}
                                    					// }, 
                                    		  // "4": {"id": "4",
                                    		  			// "name": "Disk 4",
                                    		  			// "location":"us-central1-a", 
                                    					// "disktype":"pd-standard", 
                                    					// "size": "200",
                                    					// "image": "2",
                                    					// "variables": {"var1": "4", "var2": "q"}
                                    					// }, 
                                    		  // "5": {"id": "5",
                                    		  			// "name": "Disk 5",
                                    		  			// "location":"us-central1-a", 
                                    					// "disktype":"pd-ssd", 
                                    					// "size": "300",
                                    					// "image": "1",
                                    					// "variables": {"var1": "5", "var2": "q"}
                                    					// }, 
                            			      // "6": {"id": "6",
                            			      			// "name": "Disk 6",
                            			      			// "location":"us-central1-a", 
                                    					// "disktype":"pd-standard", 
                                    					// "size": "400",
                                    					// "image": "2",
                                    					// "variables": {"var1": "6", "var2": "q"}
                                    					// }
                                    					// }
                                    		  // }
                                	// },
                    // images: {"1": {"id": "1", "name": "Image 1", "authaccount": "testauth@auth.com"}, 
                    		 // "2":{"id": "2", "name": "Image 2", "authaccount": "testauth2@auth.com"},
                    		// },
                    // credentials: {"name": "testname", "serviceaccount": "test@test.com"},
                    // }

// get workflow data
function getUserData(callback, callbackargs) {
	$.get(getBaseUrl() + 'api/_getuserdata', {}, function(data, textStatus) {
        // if (data["message"]!="none") {
        	// alert(data["message"]);	
        // }    
        WORKFLOWDATA = data["data"];
        if (!(typeof callback === "undefined")) {
        	if (typeof callbackargs === "undefined") {
        		callback();
        	} else {
        		callback(callbackargs);		
        	}
        }
        
    }, "json");
	return({});
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

// merge two object dicts
function mergeDicts(oldDict, newDict, depth) {
	if ((!(typeof newDict === 'object') & !(typeof oldDictDict === 'object')) | Array.isArray(newDict)) {
		return(newDict);
	}
	$.each(Object.keys(newDict), function(index, key) {
		if (!($.inArray(key, Object.keys(oldDict))>-1) | key=="variables" | key=="Commands" | key=="instances" | key == "disks") {
			oldDict[key] = newDict[key];
		} else {
			oldDict[key] = mergeDicts(oldDict[key], newDict[key], depth+1);
		}
	});
	return(oldDict);
}

// this function updates the global workflow data
function updateData(data, page) {
	// console.log("updating data!");
	// console.log(data);
	var updateKeys = Object.keys(data);
	$.each(updateKeys, function(index, updateKey) {
		if (!($.inArray(updateKey, Object.keys(WORKFLOWDATA))>-1)) {
			// console.log(updateKey);
			// console.log("setting update key");
			WORKFLOWDATA[updateKey] = data[updateKey];
		} else {
			// console.log(updateKey);
			// console.log("merging update key");
			WORKFLOWDATA[updateKey] = mergeDicts(WORKFLOWDATA[updateKey], data[updateKey], 0);
		}
	});
	// console.log(WORKFLOWDATA);
	
	updatePageElements(page);
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
	var currentWorkflowIDName = $("#"+workflowSelect+" :selected").html();
	if (typeof(currentWorkflowIDName)==="undefined") {return("None");}
	if (currentWorkflowIDName.indexOf(": ") < 0) {return("None");} 
    var currentWorkflowID = splitNameIntoIDAndName(currentWorkflowIDName)["id"];
    if (!($.inArray(currentWorkflowID, Object.keys(workflows))>-1)) {return("None");}
    var currentWorkflow = workflows[currentWorkflowID];
    return(currentWorkflow);
}

// get a variable in a workflow e.g. disk or instance
function getWorkflowVar(workflowSelect, varSelect, vartype) {
	var currentWorkflow = getWorkflow(workflowSelect);
	if (currentWorkflow=="None") {return("None");}
	if (typeof $("#"+varSelect+" :selected").html() === 'undefined') {return("None");}
	var varIDName = $("#"+varSelect+" :selected").html();
    var varID = splitNameIntoIDAndName(varIDName)["id"];
    // console.log(currentWorkflow);
    // console.log(vartype);
    if (!($.inArray(varID, Object.keys(currentWorkflow[vartype]))>-1)) {return("None");}
    var currentVar = currentWorkflow[vartype][varID];
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
	var varID = splitNameIntoIDAndName(varIDName)["id"];
	if ($.inArray(varID, Object.keys(images))>-1) {
		return(images[varID]);
	} else {
		return("None");
	}
	
}

// get a set of credentials
function getCredential(credSelect) {
	var credentials = getData(["credentials"]);
	var varIDName = $("#"+credSelect+" :selected").html();
	var varID = splitNameIntoIDAndName(varIDName)["id"];
	if ($.inArray(varID, Object.keys(credentials))>-1) {
		return(credentials[varID]);
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
    var command = instance["Commands"][commandID];
    return(command);
}

// get a command
function getCommandDependencies(workflowSelect, instanceSelect, commandSelect) {
	var instance = getInstance(workflowSelect, instanceSelect);
	var commandIDName = $("#"+commandSelect+" :selected").html();
	if (commandIDName == "New Command") {
		return("New Command");
	}
    var commandID = splitNameIntoIDAndName(commandIDName)["id"];
    var command = instance["Commands"][commandID];
    var dependencies = [];
    for (var i=0; i<command["dependencies"].length; i++) {
    	dependencies.push(instance["Commands"][command["dependencies"][i]]);
    }
    return(dependencies);
}

// standard naming scheme for options
function getOptions(vars, additionalOptions, selected) {
	if (typeof vars === 'undefined') { vars = [];}
	var optionnames = [];
	if (Array.isArray(vars)) {
		$.each(vars, function(index, value) {
		optionnames.push(value);
		});
	} else {
		$.each(vars, function(index, value) {
		optionnames.push(value["id"]+": "+value["name"]);
		});
	}
	if (typeof additionalOptions === 'undefined') { additionalOptions = [];}
	optionnames = optionnames.concat(additionalOptions);
	if (typeof selected === 'undefined') { 
		var toselect = optionnames[0];
	} else {
		var toselect = selected["id"]+": "+selected["name"];
	}
	var result = "";
	for (var i=0; i<optionnames.length; i++) {
		if (optionnames[i]==toselect) {
			result = result + "<option selected>";
		} else {
			result = result + "<option>";
		}
		result += optionnames[i] + "</option>";
	}
	return(result);
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
    var selecter =$("#"+elementID);
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

function getBaseUrl() {
    var re = new RegExp(/^.*\//);
    return re.exec(window.location.href)[0];
}




// a function to submit form data
function submitForm(event, submitType, editType, page, reload) {
    var formData = new FormData($(event.target).parent()[0]);
    var reload = true;
    if (typeof reload === "undefined") {
        reload = false;
    }
	formData.append("submitType", submitType);
	formData.append("editType", editType);
	// console.log(formData);
	$.ajax({
		url: getBaseUrl() + 'api/_workflows',
		data: formData,
		processData: false,
		contentType: false,
		type: 'POST',
		success: function(data){
	        if (reload) {
	        	getUserData(updatePageElements, page);
	        } else {
	        	updateData(data["updates"], page);
	        }
		}
	});
	
	// $.post(getBaseUrl() + 'api/_workfloweditor', formData, function(data, textStatus) {
        // // if (data["message"]!="none") {
        	// // alert(data["message"]);	
        // // }    
        // console.log(data["updates"]);
        // if (reload) {
        	// getUserData(updatePageElements);
        // } else {
        	// updateData(data["updates"]);
        // }     	
    // }, "json");
    // console.log("submitted form");
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
    
    var num = ($("#"+locationID).contents().length/2).toString();
    keyname = keyname + "_"+ num;
    valuename = valuename + "_" + num;
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
    addKeyValVariable(key, value, "varname", "varvalue", "workflowvars");
} 

// adds a variable to the instance
function addInstancesVar(key, value) {
    addKeyValVariable(key, value, "varname", "varvalue", "instancevars");
}

// adds a variable to the disk
function addDisksVar(key, value) {
    addKeyValVariable(key, value, "varname", "varvalue", "diskvars");
}

//// FUNCTIONS TO INITIALIZE AND UPDATE THE WORKFLOW VARIABLES FORM

// updates the workflow variables form when a new workflow is selected
function updateWorkflowVarForm() {
    var currentWorkflow = getWorkflow("workflowVarWorkflowsSelect");
    console.log(currentWorkflow);
    if (currentWorkflow!="None") {
	    // reset select
	    $("#workflowvars").html("");
	    // set variables of current workflow in form
	    var variables = Object.keys(currentWorkflow["variables"]);
	    for (var i=0; i<variables.length; i++) {
	        addWorkflowVar(variables[i], currentWorkflow["variables"][variables[i]])
	    }
	}
}

function updateWorkflowVarsOnWorkflowsForm() {
	var currentWorkflow = getWorkflow("workflowWorkflowsSelect");
    $("#newWorkflowName").val("");
    var credentials = getData(["credentials"]);
    $("#workflowCredentialsSelect").html(getOptions(credentials));
	console.log("about to set credentials");
    if (currentWorkflow!="None") {
    	console.log("setting credentials");
    	var cred = credentials[currentWorkflow["credentials"]];
    	console.log(cred["id"]+": "+cred["name"]);
    	setSelectorOption("workflowCredentialsSelect", cred["id"]+": "+cred["name"]);
    	console.log("setting name");
    	$("#newWorkflowName").val(currentWorkflow["name"]);	
    }
    
}

function initWorkflowForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#workflowWorkflowsSelect").html(getOptions(workflows, ["New Workflow"]));
    updateWorkflowVarsOnWorkflowsForm();
}

// initialize the workflow variable form
function initWorkflowVarForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#workflowVarWorkflowsSelect").html(getOptions(workflows));
    updateWorkflowVarForm();
}

//// FUNCTIONS TO INITIALIZE AND UPDATE THE INSTANCE VARIABLES FORM

function updateInstanceVariablesInInstanceVarForm() {
	$("#instancevars").html(""); // clear out old variables
    var currentInstance = getInstance("instanceVarWorkflowsSelect", "instanceVarInstancesSelect");
    if (currentInstance!="None") {
	    var instancevars = currentInstance["variables"]; // get current instance variables
	    var keys = Object.keys(instancevars); // get instance variable keys
	    // change key value pairs
	    for (var i=0; i<keys.length; i++) {
	    	addInstancesVar(keys[i], instancevars[keys[i]]);
	    }
	}
}

// update instances select in instance variable form after workflow is selected
function updateInstancesInInstanceVarForm() {
    var currentWorkflow = getWorkflow("instanceVarWorkflowsSelect");	
	// update instance select html
	$("#instanceVarInstancesSelect").html(getOptions(currentWorkflow["instances"]));	
	updateInstanceVariablesInInstanceVarForm();
}

// initialize the instance variable form
function initInstanceVarForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#instanceVarWorkflowsSelect").html(getOptions(workflows));
    updateInstancesInInstanceVarForm();
}

//// FUNCTIONS FOR THE INSTANCE FORM

function addInstanceDependency(instance) {
    var currentWorkflow = getWorkflow("instanceWorkflowsSelect");
    var instances = currentWorkflow["instances"];
    if (instance != "") {
    	var options = getOptions(instances, ["None"], instance);	
    } else {
    	var options = getOptions(instances, ["None"]);
    }
    // add disknames to select
    var toadd = "<div class=\"row\"><div class=\"form-group col-sm-6\">\n<select class=\"form-control\" name=\"instanceDependenciesSelect\">";
    var toadd = toadd + options;
    var toadd = toadd + "</select>\n</div>\n<div class=\"form-group col-sm-4\">\n<button type=\"button\" class=\"btn btn-default\" onclick=\"removeDivsDiv(this)\" >Remove</button>\n</div></div>";
    $("#InstanceDependencies").append(toadd);  
}

// add another read disk option to the instance
function addDisk(disk, type) {
    var currentWorkflow = getWorkflow("instanceWorkflowsSelect");
    if (disk!="") {
    	var orderedDiskNames = getOptions(currentWorkflow["disks"], ["None"], disk);	
    } else {
    	var orderedDiskNames = getOptions(currentWorkflow["disks"], ["None"]);
    }
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

function toggleAdvancedOptions() {
	$("#optionalInstanceParams").toggle();
}

function hideAdvancedOptions() {
	$("#optionalInstanceParams").hide();
}



// update disk options on instance form
function updateInstanceOptionsOnInstanceForm() {
    var currentInstance = getInstance("instanceWorkflowsSelect", "instanceInstancesSelect");    
    if (currentInstance != "None") {
        // console.log("resetting options!");
        // reset all disk option
        $("#instanceReadDisks").html("");    
        $("#instanceReadWriteDisks").html("");
        $("#instanceBootDisk").html("");  
        $("#InstanceDependencies").html("");     
        // set instance name
        $("#instanceName").val(currentInstance["name"]);      
        // add boot disk
        var workflow = getWorkflow("instanceWorkflowsSelect");
        addDisk(getDiskByID(workflow, currentInstance["BootDisk"]), "boot");
        // add read disks
        var readDiskNames = currentInstance["ReadDisks"];
        for (var i=0; i<readDiskNames.length; i++) {
        	// console.log("adding read disk");
        	// console.log(readDiskNames[i]);
            addDisk(getDiskByID(workflow, readDiskNames[i]), "read");
        }
        // add read write disks
        var readWriteDiskNames = currentInstance["WriteDisks"];
        for (var i=0; i<readWriteDiskNames.length; i++) {
            // console.log("adding read/write disk");
        	// console.log(readWriteDiskNames[i]);
            addDisk(getDiskByID(workflow, readWriteDiskNames[i]), "readwrite");
        }
        // set location
        setSelectorOption("instanceLocationSelector", currentInstance["location"]);
        // set machine type
        setSelectorOption("instanceMachineTypeSelector", currentInstance["machinetype"]);
        // set instance tags
        $("#ex_tags").val(currentInstance["ex_tags"]);
        // set instance metadata
        $("#ex_metadata").val(currentInstance["ex_metadata"]);
        // set instance network
        $("#ex_network").val(currentInstance["ex_network"]);
        // set number of local ssd drives
        setSelectorOption("numLocalSSD", currentInstance["numLocalSSD"]);
        // set preemptible
        $("#preemptible").prop('checked', currentInstance["preemptible"]);
        
        // set dependencies
        
    	var instances = workflow["instances"];
        var dependencies = [];
        for (var i=0;i<currentInstance["dependencies"].length; i++) {
        	dependencies.push(instances[currentInstance["dependencies"][i]]);	
        }
        for (var i=0; i< dependencies.length; i++) {
        	var dependency = dependencies[i];
        	addInstanceDependency(dependency);	
        }
        
    } else {
        // console.log("not resetting options!");
        addDisk("", "boot");
    }
}

function updatePreemptibleCheckbox() {
	if ($('#preemptible').is(':checked')) {
		console.log("setting to true");
		$("#preemptible").val("T");
	} else {
		console.log("setting to false");
		$("#preemptible").val("F");
	}
}

// initialize the instance form
function initInstanceForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#instanceWorkflowsSelect").html(getOptions(workflows));
    // update instance with instances specific to this workflow
    updateInstancesAndDisksOnInstanceForm();
    // update instance options with default first instance
    updateInstanceOptionsOnInstanceForm();
}

//// CODE FOR DISKS FORM

function updateDisksOnDiskForm() {
    var currentWorkflow = getWorkflow("diskWorkflowsSelect");
    $("#diskDisksSelect").html(getOptions(currentWorkflow["disks"], ["New Disk"]));
	updateDiskOptionsOnDiskForm();
	// "#diskWorkflowsSelect"
}

// this functions updates the disk form values when a disk is selected
function updateDiskOptionsOnDiskForm() {
    var currentDisk = getDisk("diskWorkflowsSelect", "diskDisksSelect");
    if (currentDisk != "None") {
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
        // console.log(image);
        if (typeof image ==="undefined") {
        	$("#diskImagesSelect").val("");	
        } else {
        	setSelectorOption("diskImagesSelect", image["id"]+": "+image["name"]);	
        }
    }
}

// initialize the instance variable form
function initDiskForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#diskWorkflowsSelect").html(getOptions(workflows));
    updateDisksOnDiskForm();
    // get image data
    var images = getData(["images"]);
    $("#diskImagesSelect").html(getOptions(images));
    updateDisksInDiskVarForm();
}

// this function updates the disk names in the disk var form once a workflow is selected
function updateDisksInDiskVarForm() {
    var currentWorkflow = getWorkflow("diskVarWorkflowsSelect");
    $("#diskVarDisksSelect").html(getOptions(currentWorkflow["disks"]));
    updateDiskVariablesInDiskVarForm();
}

// this function updates the disk variables in the disk variable form once a disk is selected
function updateDiskVariablesInDiskVarForm() {
    $("#diskvars").html(""); // clear out old variables
    var currentDisk = getDisk("instanceVarWorkflowsSelect", "diskVarDisksSelect");
    var diskvars = currentDisk["variables"]; // get current disk variables
    if (!(typeof diskvars === 'undefined')) {
	    var keys = Object.keys(diskvars); // get disk variable keys
	    // clear old vals
	    $("#diskvars").html("");
	    // change key value pairs
	    for (var i=0; i<keys.length; i++) {
	    	addDisksVar(keys[i], diskvars[keys[i]]);
	    }
	}
}


// initialize the instance variable form
function initDiskVarForm() {
    // get workflow data
    var workflows = getData(["workflows"]);
    // set workflow options
    $("#diskVarWorkflowsSelect").html(getOptions(workflows));
    updateDisksInDiskVarForm();
}

// update image form
function updateImageOptionsOnImageForm() {
	// get current image
	var image = getImage("imageImagesSelect");
	// reset form vars
	$("#imageNameOnImageForm").val("");
    $("#authAccount").val("");
    $("#installDirectory").val("");
    // set form vars
    if (image !="None") {
    	// get image data
	    $("#imageNameOnImageForm").val(image["name"]);
	    // set auth account
	    $("#authAccount").val(image["authaccount"]);
	    $("#installDirectory").val(image["installDirectory"]);
	}
}

// initialize images form
function initImageForm() {
    var images = getData(["images"]);
    $("#imageImagesSelect").html(getOptions(images, ["New Image"]));
	updateImageOptionsOnImageForm();
}

// update options on credentials form
function updateCredentialOptionsOnCredentialsForm() {
	// get current credential
	var credential = getCredential("credentialCredentialsSelect");

	// reset form vars
	$("#credentialsName").val("");
	$("#serviceAccountEmail").val("");
	$("#project").val("");
    
    // set form vars
    if (credential !="None") {
    	$("#credentialsName").val(credential["name"]);
		$("#serviceAccountEmail").val(credential["serviceaccount"]);
		$("#project").val(credential["project"]);
	}
}

// init credentials form
function initCredentialsForm() {
	var credentials = getData(["credentials"]);
	$("#credentialCredentialsSelect").html(getOptions(credentials, ["New Set of Credentials"]));
	updateCredentialOptionsOnCredentialsForm();

}


//// CODE FOR COMMAND DEPENDENCIES

// sets command attributes in command form
function setCommandAttributesInCommandForm() {
	// get command
    var command = getCommand("workflowInCommandForm", "instanceInCommandForm", "commandInCommandForm");
    var dependencies = getCommandDependencies("workflowInCommandForm", "instanceInCommandForm", "commandInCommandForm"); 
    // set command options
    if (command!= "New Command") {
		// set command name
		$("#CommandName").val(command["name"]);
		// set command text
		$("#Command").val(command["command"]);
		// set command dependencies
		//"4": {"id":"4", "name":"1", "command":"do d", "dependencies":["2", "3"]}
		// clear dependencies
		$("#CommandDependencies").html("");
		for (var i=0; i<dependencies.length; i++) {
			addCommandDependency(dependencies[i]);
		}
    }
}

// sets command options in command form
function setCommandOptionsInCommandForm() {
    var currentInstance = getInstance("workflowInCommandForm", "instanceInCommandForm");
    $("#commandInCommandForm").html(getOptions(currentInstance["Commands"], ["New Command"]));
    setCommandAttributesInCommandForm();
}

// sets Instance options in command form
function setInstanceOptionsInCommandForm() {
    var currentWorkflow = getWorkflow("workflowInCommandForm");
    $("#instanceInCommandForm").html(getOptions(currentWorkflow["instances"]));
	setCommandOptionsInCommandForm();
}

// initializes the command form
function initCommandsForm() {
	var workflows = getData(["workflows"]);
	$("#workflowInCommandForm").html(getOptions(workflows));
    setInstanceOptionsInCommandForm();
}

function addCommandDependency(command) {
    var currentInstance = getInstance("workflowInCommandForm", "instanceInCommandForm");
    var commands = currentInstance["Commands"];
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

//// CODE FOR LAUNCHER PAGE

// Array.prototype.diff = function(a) {
    // return this.filter(function(i) {return a.indexOf(i) < 0;});
// };

function initLauncherWorkflowForm() {
	// console.log("initializing launcher form");
	var activeWorkflows = getData(["active_workflows"]);
	console.log("active workflows");
	console.log(activeWorkflows);
	$("#activeWorkflowSelect").html(getOptions(activeWorkflows));
	var workflows = getData(["workflows"]);
	console.log("workflows");
	console.log(workflows);
	console.log(Object.keys(workflows));
	var inactiveworkflows = {};
	var inactiveKeys = [];
	for (key in Object.keys(workflows)) {
		if ($.inArray(key, Object.keys(activeWorkflows))) {
			inactiveKeys = inactiveKeys.concat([key]);
		}
	}
	// var inactiveKeys = Object.keys(workflows).diff(Object.keys(activeWorkflows));
	console.log("inactiveKeys");
	console.log(inactiveKeys);
	for (key in inactiveKeys) {
		inactiveworkflows[key] = workflows[key];
	}
	console.log("inactiveworkflows");
	console.log(inactiveworkflows);
	$("#launcherWorkflowSelect").html(getOptions(inactiveworkflows));
}

//// CODE FOR DASHBOARD PAGE

function isEmpty(obj) {
    // null and undefined are "empty"
    if (obj == null) return true;
    // Assume if it has a length property with a non-zero value
    // that that property is correct.
    if (obj.length > 0)    return false;
    if (obj.length === 0)  return true;
    // Otherwise, does it have any properties of its own?
    // Note that this doesn't handle
    // toString and valueOf enumeration bugs in IE < 9
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }
    return true;
}

// generic make gviz table function
function drawtable(data, elementid, jscode_data) {
	if (!isEmpty(data)) {
		// console.log(data);
		$.each(data.colnames, function(k) {
			var col = data.colnames[k];
			var type = col[0];
			var key = col[1];
			var name = col[2]; 
			jscode_data.addColumn(type, name, key);
		});
		jscode_data.addRows(data.numrows);
		var i = 0;
		$.each(data.rows, function(l) {
			j=0;
			var row = data.rows[l];
			$.each(data.colnames, function(k) {
				var col = data.colnames[k];
				var type = col[0];
				var key = col[1];
				var name = col[2]; 
				// console.log(row[key]["value"]);
				// console.log(row[key]["css"]);
				jscode_data.setCell(i, j, row[key]["value"]);
				jscode_data.setProperty(i, j, 'style', row[key]["css"]);
				j+=1;
			});
			i+=1;
		});
		// console.log(elementid);
		// console.log(jscode_data);
		jscode_table = new google.visualization.Table(document.getElementById(elementid));
		jscode_table.draw(jscode_data, {showRowNumber: false, allowHtml: true});
		return jscode_data, jscode_table;			
	} else {
		$("#"+elementid).html("");
	}
}

// some javascript to generate gviz datatables for variant, clinical trial, guidelines info, etc
function getDashboardData(data_type, data, callback) {
	console.log(data_type)
	console.log(data);
	data["type"]=data_type;
	$.get(getBaseUrl() + 'api/_getdashboarddata', data, function(data, textStatus) {
        //if (data["message"]!="") {alert(data["message"]);}
		console.log(data);
		callback(data["data"]);
    }, "json");
}

function drawChart(raw_data, options, element_id) {
	var columns = raw_data[1];
	var dashboard = new google.visualization.Dashboard(
		document.getElementById('perf_dashboard'));
	var dashboardDataSelector = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'dashboard_selector',
          'options': {
            'filterColumnLabel': 'Time (min)'
          }});
    var cpuChart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'cpu_chart',
          'options': {legend: {position: 'bottom'},
          			  series: {0: { color: '#e2431e'}}
          			  },
          'view': {'columns': [0, 1]}
        });
    var memChart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'mem_chart',
          'options': {legend: {position: 'bottom'},
          			  series: {0: { color: '#e7711b'}}
          			  },
          'view': {'columns': [0, 2]}
        });
    var memgbChart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'memgb_chart',
          'options': {legend: {position: 'bottom'},
          			  series: {0: { color: '#f1ca3a'}}
          			  },
          'view': {'columns': [0, 3]}
        });
    var readChart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'read_chart',
          'options': {legend: {position: 'bottom'},
          			  series: {0: { color: '#6f9654'}}
          			  },
          'view': {'columns': [0, 4]}
        });
    var writeChart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'write_chart',
          'options': {legend: {position: 'bottom'},
          			  series: {0: { color: '#1c91c0'}}
          			  },
          'view': {'columns': [0, 5]}
        });
    dashboard.bind(dashboardDataSelector, cpuChart);
    dashboard.bind(dashboardDataSelector, memChart);
    dashboard.bind(dashboardDataSelector, memgbChart);
    dashboard.bind(dashboardDataSelector, readChart);
    dashboard.bind(dashboardDataSelector, writeChart);
    var data = google.visualization.arrayToDataTable(raw_data);
    dashboard.draw(data);
    
	
	// var chart = new google.visualization.LineChart(document.getElementById(element_id));
    // chart.draw(data, options);
}	

function toggleCommand(workflow_id, instance_id, command_id) {
	getDashboardData("performance", {"instance_id":instance_id, 
	"command_id":command_id, "workflow_id":workflow_id}, function(chart_data) {
		var options = {
			// title: 'Command Performance',
			// curveType: 'function',
			legend: {position: 'bottom'}
		};
		drawChart(chart_data, options, "command_chart");
	});
}

function toggleCommands(workflow_id, instance_id) {
	getDashboardData("commands", {"instance_id":instance_id, "workflow_id":workflow_id}, function(table_data) {
		var jscode_data = new google.visualization.DataTable();
		drawtable(table_data, "commands_table", jscode_data);	
	});
}

// draw instances table
function setInstancesData(workflow_id) {
	getDashboardData("instances", {"workflow_id":workflow_id}, function(table_data) {
		var jscode_data = new google.visualization.DataTable();
		drawtable(table_data, "instances_table", jscode_data);	
	});
}

// update instances upon instance name selection
function updateDashboardInstances() {
	setInstancesData(splitNameIntoIDAndName($("#dashboardWorkflowNameSelect").val())["id"]);	
}


// updates the workflow selectors on the dashboard page
function updateDashboardWorkflowSelect(workflows) {
	var workflow_id = splitNameIntoIDAndName($("#dashboardWorkflowSelect").val())["id"];
	var workflownames = workflows[workflow_id]["names"];
	$("#dashboardWorkflowNameSelect").html(getOptions(workflownames));
	setInstancesData(splitNameIntoIDAndName($("#dashboardWorkflowNameSelect").val())["id"]);
}

// update without initializing first
function updateDashboardWorkflowsSelectWithoutInit() {
	getDashboardData("workflows", {}, function(workflows) {
		updateDashboardWorkflowSelect(workflows);	
	}); 
}

// initializes the dashboard page
function initDashboard() {
	getDashboardData("workflows", {}, function(workflows) {
		console.log(getOptions(workflows));
		$("#dashboardWorkflowSelect").html(getOptions(workflows));
		updateDashboardWorkflowSelect(workflows);	
	}); 
}


//// CODE TO RUN ON PAGE LOADING

function updatePageElements(page) {
    // console.log(page);
    if (page=="setup") {
    	initCredentialsForm();
	    initWorkflowForm();
	    initWorkflowVarForm();
	    initInstanceForm();
	    initInstanceVarForm();
	    initDiskVarForm();
	    initDiskForm();
	    initImageForm();
	    initCommandsForm();	
	    //toggleAdvancedOptions();
	    hideAdvancedOptions();
    } else if (page=="launcher") {
    	initLauncherWorkflowForm();
    } else if (page =="dashboard") {
    	console.log("dashboard");
    	initDashboard();
    }
    	
}

// $(document).ready(function(){
	// // this code sets the write view on startup
    // toggleView("workflows_section");
    // $(".nav li").on("click", function() {
        // $(".nav li").removeClass("active");
        // $(this).addClass("active");
    // });
	// getUserData(updatePageElements);
// });


 