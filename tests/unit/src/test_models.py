import pytest
import uuid
import json
from src.models import *
from . import *

def test_model_instantiate_success():
    m = Model()
    assert isinstance(m, Model)
    assert isinstance(m.guid, str)

def test_model_instantiate_otherdata():
    m = Model(foo='bar')
    assert isinstance(m, Model)

def test_response_dump():
    pass

def test_model_instantate_dict():
    data = get_mock_model()
    m = Model(**data)
    assert m.guid == 'b1e0e990-7ac5-4711-9a33-97d11403f7f7'
    assert m.name == 'martha'
    assert 'foo' in m.metadata

def test_model_store_get(models_store):
    m = Model(guid=get_known_id())
    name = get_known_name()
    response: Response = models_store.get(m, None)
    assert response.statusCode == 200
    assert len(response.body.models) == 1
    assert response.body.models[0].name == name

def test_model_store_get_all(models_store):
    name = get_known_name(1)
    response: Response = models_store.get_all(None)
    assert response.statusCode == 200
    assert len(response.body.models) == 3
    assert response.body.models[1].name == name

def test_model_store_post_empty(models_store):
    model = Model()
    response: Response = models_store.post(model, None)
    assert response.statusCode == 200
    assert len(response.body.models) == 1
    assert response.body.models[0].guid == model.guid
    response: Response = models_store.get_all(None)
    assert response.statusCode == 200
    assert len(response.body.models) == 4
    assert response.body.models[3].guid == model.guid

def test_model_store_post_data(models_store):
    model = Model(name='Elizabeth', metadata={'foo': 'biz'})
    response: Response = models_store.post(model, None)
    assert response.statusCode == 200
    assert len(response.body.models) == 1
    assert response.body.models[0].guid == model.guid
    response: Response = models_store.get_all(None)
    assert response.statusCode == 200
    assert len(response.body.models) == 5
    assert response.body.models[4].name == model.name

def test_model_store_post_exist(models_store):
    guid = get_known_id(0)
    model = Model(guid=guid, name='Elizabeth', metadata={'foo': 'biz'})
    response: Response = models_store.post(model, None)
    assert response.statusCode == 400
    assert len(response.body.models) == 0
    assert len(response.body.errors) == 1
    response: Response = models_store.get_all(None)
    assert response.statusCode == 200
    assert len(response.body.models) == 5

def test_model_store_put_known(models_store):
    data = get_mock_model(1)
    model = Model(**data)
    guid = model.guid
    model.name = "louise"
    response: Response = models_store.put(model, None)
    assert response.statusCode == 200
    assert len(response.body.models) == 2
    assert response.body.models[0].guid == response.body.models[1].guid 
    assert response.body.models[0].name != response.body.models[1].name    

def test_model_store_put_unknown(models_store):
    model = Model(
        guid= '00000000-0000-0000-0000-000000000000',
        name="bill",
        metadata={'foo': 'apple'}
    )
    response: Response = models_store.put(model, None)
    assert response.statusCode == 400
    assert len(response.body.models) == 0
    assert len(response.body.errors) == 1

def test_model_store_delete_known(models_store):
    guid = get_known_id(0) 
    model = Model(guid=guid)
    response: Response = models_store.delete(model, None)
    assert response.statusCode == 200
    assert len(response.body.models) == 1

def test_model_store_delete_unknown(models_store):
    model = Model(
        guid= '00000000-0000-0000-0000-000000000000'
    )
    response: Response = models_store.delete(model, None)
    assert response.statusCode == 400
    assert len(response.body.models) == 0
    assert len(response.body.errors) == 1