
import os
import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.typing import LambdaContext
from models import Model, ModelStore, Response, ModelError
from typing import Any, Dict, List


log_level=os.environ.get("LOG_LEVEL", 'ERROR').upper()
logger = Logger(service="model-api", level=log_level)

ddb_table_name = os.environ.get('DDB_TABLE_NAME', "models")

model_store = None

#decorator logs context info and the full event ( default event logging is false)
@logger.inject_lambda_context(log_event=True)
def router(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    global model_store
    # make the connection to dynamodb if not yet done.
    if model_store is None:
        model_store = ModelStore(ddb_table_name)
    
    # use powertools to structure and validate event
    event: APIGatewayProxyEventV2 = APIGatewayProxyEventV2(event)
    request_context = event.request_context
    query_string_parameters = event.query_string_parameters
    response = Response()
    if 'models' in event.raw_path:
        if event.body is None:
            body = dict()
        else:
            body = json.loads(event.body)
        # need to catch empty guid for get all, but also create new Model with new guid when post
        has_guid = bool(body.get('guid', None))
        # use powertools to parse event.body into a Model
        model: Model = parse(event=body, model=Model)
        
        # POST
        if request_context.http.method == 'POST':
            response = model_store.post(model, query_string_parameters)
        # GET
        elif request_context.http.method == 'GET':
            if has_guid: # looking for one model
                response = model_store.get(model, query_string_parameters)
            else: # want all the models
                response = model_store.get_all(query_string_parameters)
        # PUT
        elif request_context.http.method == 'PUT':
            response = model_store.put(model, query_string_parameters)
        # DELETE
        elif request_context.http.method == 'DELETE':
            response = model_store.delete(model, query_string_parameters)
    else:
        err = ModelError(
            status=400,
            title="wrong path endpoint requested",
            details=f"the path requested {event.raw_path} does not contain 'models'"
        )
        response.add_model_error(err)
    return response.dump()