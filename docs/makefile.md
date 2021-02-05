# Makefile
This makefile is meant to ease the use of managing dependencies and building the layer archive (zip) for deployment.  
Running make with no target will give you a list of the available targets and their purpose.  
You must also have two environment variables defined and exported or written in a `.env` file for   
layer processing to execute correctly. See the [Config](/dotenv) doc for more details. 
The environment variables required for layer archive creation are:

* LAYER_VERSION: semantic versioning suffix for layer archive name, used by make and by cdk  
* LAYER_NAME: prefix on the layer archive file (zip) used by make and cdk  

## Targets in the makefile
* list (or just make) -- list all the targets in this file with a description
* deps  -- rebuild both venv and local layer
* clean -- rm cdk, layer, and venv
* venv -- rebuild venv from scratch
* layer -- build clean layer zip
* test -- runs tests on lambda src and cdk stacks
* test-src -- runs pytest and cdk synth
* test-cdk -- executes cdk synth
* build-venv -- create venv if not there
* pip-venv -- install reqs into venv
* pip-layer -- install reqs into local dir for layer
* zip-layer -- zip up the layer packages for asset deployment
* clean-cdk -- clean the cdk.out dir
* clean-layer -- clean the layer libs
* clean-venv -- clean the venv dir