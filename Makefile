ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# this will list all the targets in this makefile by default or by make list
# putting a '## comment on a target line will add a description to output
.DEFAUL_GOAL := list
.PHONY: list

list: 
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)##\(.*\)/\1\3/p' 

all: venv layer ##  -- rebuild both venv and local layer
.PHONY: all

clean: clean-cdk clean-venv clean-layer ## -- rm cdk, layer, and venv
.PHONY: clean

venv: clean-venv build-venv pip-venv ## -- rebuild venv from scratch
.PHONY: venv

layer: clean-layer pip-layer zip-layer ## -- build clean layer zip
.PHONY: layer

test: test-src test-cdk ## -- runs tests on lambda src and cdk stacks
.PHONY: test

test-src: ## -- runs pytest and cdk synth
	@ echo "running tests with coverage"
	@ pytest -rP --cov=src 

test-cdk: ## -- executes cdk synth
	@ echo "doing cdk synth"
	@ cdk synth

build-venv: ## -- create venv if not there
	@ echo "deploying virtual env to .venv"
	@ if [ ! -d .venv ]; then python3 -m venv .venv; else echo "venv already provisioned"; fi

pip-venv: ## -- install reqs into venv
	@ echo "installing python requirements for venv"
	@ source .venv/bin/activate; pip install -U -r ./requirements.txt

pip-layer: ## -- install reqs into local dir for layer
	@ echo "installing python requirements for layers"
	@ if [ ! -d layers/python ]; then mkdir -p layers/python/lib/python3.8/site-packages; fi
	@ source .venv/bin/activate; pip install -U -t layers/python/lib/python3.8/site-packages/ -r layers/requirements.txt 

zip-layer: ## -- zip up the layer packages for asset deployment
	@ echo "creating zip file of layer requirements"
	@ cd layers; zip -r ${LAYER_NAME}_${LAYER_VERSION}.zip .

clean-cdk: ## -- clean the cdk.out dir
	@ echo "removing cdk.out"
	@ rm -rf cdk.out

clean-layer: ## -- clean the layer libs
	@ echo "removing layer libs"
	@ cd layers; rm -rf python; rm *.zip

clean-venv: ## -- clean the venv dir
	@ echo "removing .venv "
	@ rm -rf .venv