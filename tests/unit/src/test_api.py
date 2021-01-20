import pytest
import uuid
import json

from . import *

def test_api_handler_get_known(models_store, lambda_context):
    from src import api
    guid = get_known_id()
    name = get_known_name()
    api.model_store = models_store
    event = api_gateway_event_v2(payload={'guid':guid}, path="models", method="GET")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 0
    assert len(body['models']) == 1
    model = body['models'][0]
    assert model['guid'] == guid
    assert model['name'] == name

def test_api_handler_get_unknown(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    event = api_gateway_event_v2(payload={'guid': '00000000-0000-0000-0000-000000000000'}, path="models", method="GET")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 1
    assert len(body['models']) == 0

def test_api_handler_get_all(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    event = api_gateway_event_v2(payload={}, path="models", method="GET")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 0
    assert len(body['models']) == 3

def test_api_handler_put_known(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    model = get_mock_model()
    model['name'] = "martha dandridge"
    event = api_gateway_event_v2(payload=model, path="models", method="PUT")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 0
    assert len(body['models']) == 2
    old_name = body['models'][0]['name']
    new_name = body['models'][1]['name']
    print (f"old: {old_name} vs new: {new_name}")
    assert  old_name != new_name

def test_api_handler_put_unknown(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    model = get_mock_model_unknown()
    event = api_gateway_event_v2(payload=model, path="models", method="PUT")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 1
    assert len(body['models']) == 0

def test_api_handler_post_empty(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    event = api_gateway_event_v2(payload={}, path="models", method="POST")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 0
    assert len(body['models']) == 1
    print(f"model: {body['models'][0]}")

def test_api_handler_post_known_partial(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    model ={
        "name": "sally",
        "metadata" : { "toast": "avocado"}
    }
    event = api_gateway_event_v2(payload=model, path="models", method="POST")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 0
    assert len(body['models']) == 1
    print(f"model: {body['models'][0]}")

def test_api_handler_post_unknown_full(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    model = get_mock_model_unknown()
    event = api_gateway_event_v2(payload=model, path="models", method="POST")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 0
    assert len(body['models']) == 1
    print(f"model: {body['models'][0]}")


def test_api_handler_post_known_full(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    model = get_mock_model()
    event = api_gateway_event_v2(payload=model, path="models", method="POST")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 1
    assert len(body['models']) == 0


def test_api_handler_delete_known(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    model = get_mock_model()
    event = api_gateway_event_v2(payload=model, path="models", method="DELETE")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 0
    assert len(body['models']) == 1
    print(f"model: {body['models'][0]}")
    # Confirm model removed from db, request should fail
    event = api_gateway_event_v2(payload=model, path="models", method="GET")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 1

def test_api_handler_delete_unknown(models_store, lambda_context):
    from src import api
    api.model_store = models_store
    model = get_mock_model_unknown()
    event = api_gateway_event_v2(payload=model, path="models", method="DELETE")
    response = api.router(event, lambda_context)
    assert isinstance(response, dict)
    assert 'body' in response
    body = json.loads(response['body'])
    assert len(body['errors']) == 1
    assert len(body['models']) == 0