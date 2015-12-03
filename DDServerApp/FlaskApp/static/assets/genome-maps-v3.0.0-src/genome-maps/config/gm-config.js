/**
 * This is a configuration file.
 * Changes to this file may cause the application does not work as it should
 *
 * Default hosts
 * CELLBASE_HOST = "http://usa.cellbase.org:8080/cellbase/rest";
 * CELLBASE_HOST = "http://ws.bioinfo.cipf.es/cellbase/rest";
 * OPENCGA_HOST = "http://ws.bioinfo.cipf.es/gcsa/rest";
 *
 * Deprecated hosts
 * WUM_HOST = "http://ws.bioinfo.cipf.es/wum/rest";
 *
 **/
// CELLBASE_HOST = "http://ws.bioinfo.cipf.es/cellbase/rest";
CELLBASE_HOST = "http://127.0.0.1:5000/cellbase/rest";
//OPENCGA_HOST = "http://ws.bioinfo.cipf.es/opencga/rest";
OPENCGA_HOST = "http://ws-beta.bioinfo.cipf.es/opencga/rest";
// OPENCGA_HOST = "http://localhost:61976/opencga/rest"
// OPENCGA_LOCALHOST = "http://localhost:61976/opencga/rest";
OPENCGA_LOCALHOST = "http://127.0.0.1:5000/opencga/rest";

/** List of available species in the cellbase service **/
var AVAILABLE_SPECIES = [
                        {	"name":"Homo sapiens 37.p7", "species":"hsa", "icon":"",
							"region":{"chromosome":"7","start":140482800,"end":140482900}
						}
                        ];

/** Reference to a species from the list to be shown at start **/
var DEFAULT_SPECIES = AVAILABLE_SPECIES[0];

var SPECIES_TRACKS_GROUP = {"hsa":"group1"
							};

var TRACKS ={"group1":[
			          {"category":"Core",
					   "tracks":[
//					          {"id":"Cytoband", "disabled":false, "checked":true},
					          {"id":"Sequence", "disabled":false, "checked":true},
					          // {"id":"Gene/Transcript", "disabled":false, "checked":false},
			                  // {"id":"CpG islands", "disabled":false, "checked":false}
			                  ]
					  }
					  // ,
					  // {"category":"Variation",
					   // "tracks":[
			                  // {"id":"SNP", "disabled":false, "checked":false},
			                  // {"id":"Mutation", "disabled":false, "checked":false},
			                  // {"id":"Structural variation (<20Kb)", "disabled":false, "checked":false},
			                  // {"id":"Structural variation (>20Kb)", "disabled":false, "checked":false}
			                  // ]
					  // },
					  // {"category":"Regulatory",
					   // "tracks":[
					          // {"id":"TFBS", "disabled":false, "checked":false},
			                  // {"id":"miRNA targets", "disabled":false, "checked":false},
//			                  {"id":"Histone", "disabled":false, "checked":false},
//			                  {"id":"Polymerase", "disabled":false, "checked":false},
//			                  {"id":"Open Chromatin", "disabled":true, "checked":false},
			                  // {"id":"Conserved regions", "disabled":false, "checked":false}
			                  // ]
					  // }
			]
};

var DAS_TRACKS = [
				{"species":"hsa",
				   "categories":[
				      // {"name":"Core",
					   // "sources":[
                	        // {"name":"GRC Region GRCh37","url":"http://das.sanger.ac.uk/das/grc_region_GRCh37/features","checked":false},
                	        // {"name":"Vega genes","url":"http://das.sanger.ac.uk/das/vega_ens_zv8_genes/features","checked":false}
                	        // ]
				      // },
				      // {"name":"Variation",
					   // "sources":[
                	        // {"name":"Cosmic Mutations GRCh37","url":"http://das.sanger.ac.uk/das/cosmic_mutations_GRCh37/features","checked":false}
                	        // ]
				      // },
				      // {"name":"Regulatory",
					   // "sources":[]
				      // }
				   ]
				}
				];
