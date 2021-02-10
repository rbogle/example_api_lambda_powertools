#  Lambda-DynamoDB based API with AWS lambda powertools

This is a example project for an AWS serverless API deployed with CDK and written in python.

It uses:

- lambdas for integration with http api gateway, see [api](/docs/api.md) and [refs/api](docs/refs/api.md)
- lambda layers to manage dependencies, see [layers](/docs/layers.md)
  - including [AWS Powertools library](https://awslabs.github.io/aws-lambda-powertools-python/) as a micro-framework
- dynamodb for persistence, see [refs/models](/docs/refs/models.md)
- dynamodb streams to generate api triggered change events, see [refs/events](/docs/refs/events.md)
- cdk to deploy the infrastructure, see [deploy](/docs/deploy.md)
- standard mkdocs static docs generator, see [docs](/docs/docs.md)
- mkdocstrings plugin to generate documentation from the source files. 

## Configuration

You will need to have a .env file created in the root of this project to properly configure and deploy the stacks, see [config](/docs/dotenv.md) for details on the variables exported and used. 

## Setup and deployment instructions

You can use the included makefile to quickly setup the environment, test and deploy the environment, see [deploy](/docs/deploy.md) for instructions on setup and deployment and the [makefile](/docs/makefile.md) for details the make targets available. 

