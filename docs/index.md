
#  CRUD Lambda API 

This is a example project for an AWS serverless API deployed with CDK and written in python.

It uses:

- lambdas for integration with http api gateway, [api](api.md) and [refs/api](refs/api.md)
- lambda layers to manage dependencies [layers](layers.md)
  - including AWS Powertools library as a micro-framework
- dynamodb for persistence [refs/models](refs/models.md)
- dynamodb streams to generate api triggered change events, see [refs/events](refs/events.md)
- cdk to deploy the infrastructure, see [deploy](deploy.md)
- standard mkdocs static docs generator [docs](docs.md)
- mkdocstrings plugin to generate documentation from the source files. 

## Makefile setup and deployment instructions

You can use the included makefile to quickly setup the environment, test and deploy the environment.  
You will need to have a .env file created in the root of this project, see [.env](dotenv.md) for details.  
Additionally, you will need to have the make system installed on your workstation.   
  
To build the virtual environment and install the dependencies as well as build the layer zip file for deployment:
```
$ make deps
```
After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

At this point you can now test the code and synthesize the CloudFormation template for this code.

```
$ make test
```

And finally, manually deploy

```
$ make deploy
```

For documentation of the full set of makefile targets included see: [Makefile](makefile.md).

## Standard CDK setup Instructions
To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
