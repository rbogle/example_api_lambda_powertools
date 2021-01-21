#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from aws_cdk import core
from infra.infra_stack import InfraStack

load_dotenv()

stack_name = os.getenv("STACK_NAME")
account=os.getenv("DEPLOY_ACCOUNT")
region=os.getenv("DEPLOY_REGION")
env = core.Environment(account=account, region=region)

app = core.App()
InfraStack(app, stack_name, env=env)

app.synth()
