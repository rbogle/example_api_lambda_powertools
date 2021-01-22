from os import supports_follow_symlinks
import pytest
import json
import datetime
from src.models import *
from . import *

def test_dump_change_event():

    old_mod = Model(name='old')
    new_mod = old_mod.copy()
    new_mod.name ="new"
    evt_type = "MODIFY"

    med = ModelEventDetail(
        model_id=new_mod.guid,
        event_type=evt_type,
        old_model=old_mod,
        new_model=new_mod,
    )

    me = ModelChangeEvent(detail_type="foo.bar",detail=med)
    dump = me.dump()
    assert isinstance(dump['detail'], str)

def test_dynamo_handler():
    pass