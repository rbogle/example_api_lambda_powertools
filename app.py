#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from aws_cdk import core
from infra.infra_stack import InfraStack

load_dotenv()

stack_name = os.getenv("STACK_NAME")

app = core.App()
InfraStack(app, stack_name)

app.synth()
