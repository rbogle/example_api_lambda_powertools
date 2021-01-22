
import os
import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes.dynamo_db_stream_event import DynamoDBStreamEvent, DynamoDBRecordEventName
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from botocore.exceptions import ClientError
from pydantic.typing import NoneType
from models import Model, ModelChangeEvent, Response, ModelError
from typing import Any, Dict, List

log_level=os.environ.get("LOG_LEVEL", 'ERROR').upper()
logger = Logger(service="model-events", level=log_level)

eventbridge = None

#decorator logs context info and the full event ( default event logging is false)
@logger.inject_lambda_context(log_event=True)
def dynamo_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    global eventbridge
    if eventbridge is None:
        eventbridge = boto3.client("events")

    response = Response()
    event: DynamoDBStreamEvent = DynamoDBStreamEvent(event)
    logger.info(f"Event Recived: {event}")
    for record in event.records:
        event: ModelChangeEvent = None
        if record.event_name == DynamoDBRecordEventName.INSERT:
            event=ModelChangeEvent.from_dynamodb_record("CREATE", record)
        elif record.event_name == DynamoDBRecordEventName.MODIFY:
            event=ModelChangeEvent.from_dynamodb_record("UPDATE", record)
        elif record.event_name == DynamoDBRecordEventName.REMOVE:
            event=ModelChangeEvent.from_dynamodb_record("DELETE", record)
        try:
            event.send(eventbridge)
        except ClientError as ce:
            response.add_boto_error(ce)
            logger.error(ce)
        except AttributeError as ae:
            me = ModelError(
                title= "Empty ModelChangeEvent Object",
                status=500,
                detail=str(ae)
            )
            response.add_model_error(me)
            logger.error(ae)
    return response.dump()
