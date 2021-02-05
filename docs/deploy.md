# Infrastructure as Code with CDK
This project uses cdk to deploy the full service stack.  

The CDK app `app.py` and cdk stacks `infra_stack.py` included under `infra` are used together to create the services in aws for this api microservice.

See [Reference/CDK Infra](/refs/infra) for details on the constructs created and deployed. 

## Makefile setup and deployment instructions

You can use the included makefile to quickly setup the environment, test and deploy the environment.  
You will need to have a .env file created in the root of this project, see [.env](/Config) for details.  
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

For documentation of the full set of makefile targets included see: [Makefile](/Makefile).