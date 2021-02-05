# .env reference
This project uses a .env file to configure both the infrastructure stacks and the makefile processes it requires the following values to be defined.

- LAYER_VERSION: semantic versioning suffix for layer archive name, used by make and by cdk
- LAYER_NAME: prefix on the layer archive file (zip) used by make and cdk
- STACK_NAME: used by cdk to name the stack and stack resources
- LOG_LEVEL: sets logging level in the lambdas
- DEPLOY_ACCOUNT: AWS account id to deploy in
- DEPLOY_REGION: AWS region to deploy to
