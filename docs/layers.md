# Layers
This project uses lambda layers to help deploy and manage dependencies for the lambdas.

The main dependency used is the [AWS lambda powertools library](https://awslabs.github.io/aws-lambda-powertools-python) which provides extremely useful classes, decorators and methods for: 

- simplifying the use of metrics, logging and x-ray tracing   
- validating and parsing common AWS service event/request types
- including pydantic data models for custom business logic, parsing and validation

## Configuring and Packaging
This project uses a [makefile](makefile.md) to simplify the installation of the required libraries and the archive (zip) creation for deploying the layer to AWS. 

A `requirements.txt` file is included and versioned in the `layers` folder to manage those dependencies separately from the development dependencies in the root requirements file. 

The environment variables required for layer archive creation are:

* LAYER_VERSION: semantic versioning suffix for layer archive name, used by make and by cdk  
* LAYER_NAME: prefix on the layer archive file (zip) used by make and cdk  