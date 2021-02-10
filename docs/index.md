
#  Lambda-DynamoDB based API with AWS lambda powertools

This is a example project for an AWS serverless API deployed with CDK and written in python.

It uses:

- lambdas for integration with http api gateway, see [api](api.md) and [refs/api](refs/api.md)
- lambda layers to manage dependencies, see [layers](layers.md)
  - including [AWS Powertools library](https://awslabs.github.io/aws-lambda-powertools-python/) as a micro-framework
- dynamodb for persistence, see [refs/models](refs/models.md)
- dynamodb streams to generate api triggered change events, see [refs/events](refs/events.md)
- cdk to deploy the infrastructure, see [deploy](deploy.md)
- standard mkdocs static docs generator, see [docs](docs.md)
- mkdocstrings plugin to generate documentation from the source files. 

## Configuration

You will need to have a .env file created in the root of this project to properly configure and deploy the stacks, see [config](dotenv.md) for details on the variables exported and used. 

## Setup and deployment instructions

You can use the included makefile to quickly setup the environment, test and deploy the environment, see [deploy](deploy.md) for instructions on setup and deployment and the [makefile](makefile.md) for details the make targets available. 