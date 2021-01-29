
from src.models import *
from aws_lambda_powertools.utilities.parser.models import DynamoDBStreamModel, DynamoDBStreamRecordModel
from aws_lambda_powertools.utilities.parser import parse
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

    me = ModelChangeEvent(DetailType="foo.bar",Detail=med)
    dump = me.dump()
    assert isinstance(dump['Detail'], str)

def test_event_from_dynamodb():
    in_evt = get_dynamodb_stream_event()
    model: DynamoDBStreamModel = parse( model=DynamoDBStreamModel, event=in_evt)
    record = model.Records[0]
    model_change_evt: ModelChangeEvent = ModelChangeEvent.from_dynamodb_record("CREATE", record)
    assert model_change_evt.Detail.event_type =="CREATE"
    assert model_change_evt.Detail.model_id =='60a5de7e-17ea-411e-b092-0652646f9d3a'

def test_dynamo_handler():
    pass