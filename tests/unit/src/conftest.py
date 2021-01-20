import pytest
import boto3
from collections import namedtuple
import os
from moto import mock_dynamodb2
from . import *


@pytest.fixture(scope="module")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

@pytest.fixture(scope="module")
def ddb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.resource('dynamodb', region_name="us-east-1")

@pytest.fixture(scope="module")
def ddb_table(ddb):
    """Create a DynamoDB surveys table fixture."""
    table = ddb.create_table(
        TableName='models',
        KeySchema=[
            {
                'AttributeName': 'guid',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'guid',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='models')

    items = get_model_set()
    for item in items:
        table.put_item(Item=item)

    yield 

@pytest.fixture(scope="module")
def models_store(ddb_table):
    from src.models import ModelStore
    modelstore = ModelStore()
    yield modelstore

@pytest.fixture(scope="module")
def lambda_context():
    lambda_context = {
        "function_name": "router",
        "memory_limit_in_mb": 128,
        "invoked_function_arn": "arn:aws:lambda:us-east-1:809313241:function:router",
        "aws_request_id": "52fdfc07-2182-154f-163f-5f0f9a621d72",
    }
    return namedtuple("LambdaContext", lambda_context.keys())(*lambda_context.values())