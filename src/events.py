from logging import log
import os
from typing import Any, Dict, List
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser.models import DynamoDBStreamModel
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from botocore.exceptions import ClientError
from models import Model, ModelChangeEvent, Response, ModelError


log_level=os.environ.get("LOG_LEVEL", 'ERROR').upper()
logger = Logger(service="model-events", level=log_level)

eventbridge = None

#decorator logs context info and the full event as json ( default event logging is false)
@logger.inject_lambda_context(log_event=True)
def dynamo_stream_handler(in_event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """ This method when registered as a lambda will handle incoming dynamodb stream events
        from a connected dynamodb. It transforms those events using the ModelChangeEvent model
        and puts them out to eventbridge as a custom event. This way business logic for change 
        events are encapsulated in the models package.

    Args:
        in_event (Dict[str, Any]): the incoming event
        context (LambdaContext): the context

    Returns:
        Dict[str, Any]: Response converted to dict, not typically consumed 
    """
    global eventbridge
    if eventbridge is None:
        eventbridge = boto3.client("events")

    response = Response()
    ddb_model: DynamoDBStreamModel = parse( model=DynamoDBStreamModel, event=in_event)
    logger.info(f"DynamodbStreamEvent Received: {ddb_model}")
    for record in ddb_model.Records:
        out_event: ModelChangeEvent = None
        if record.eventName == 'INSERT':
            out_event=ModelChangeEvent.from_dynamodb_record("CREATE", record)
        elif record.eventName == 'MODIFY':
            out_event=ModelChangeEvent.from_dynamodb_record("UPDATE", record)
        elif record.eventName == 'REMOVE':
            out_event=ModelChangeEvent.from_dynamodb_record("DELETE", record)
        try:
            logger.info(out_event)
            result = out_event.send(eventbridge)
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
        else:
            logger.info(result)
    return response.dump()
