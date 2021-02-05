from datetime import datetime
from uuid import UUID, uuid4
from typing import List,Dict, Optional
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from dynamodb_json import json_util 
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import BaseModel, Field, validator
from aws_lambda_powertools.utilities.parser.models import DynamoDBStreamRecordModel, DynamoDBStreamChangedRecordModel


class Model(BaseModel):
    """ This class is the model of our API domain object 

    Attributes:
        guid (str): a generated uuid4 string
        name (str): name for this objec
        metadata (dict): dictionary for arbitrary data of the object

    """
    guid: str = Field(default_factory= lambda: str(uuid4()))
    name: str = None
    metadata: dict = None

    @validator('guid')
    def validate_guid(cls, g:str) -> str:
        """ This fuction validates guid arg passed to constructor 
            It will catch a ValueError on conversion to UUID, and 
            generate a new uuid4 in its place. 

        Args:
            g (str): str passed to constructor for guid

        Returns:
            str: returns a true string instance of a hex representation of a uuid4
        """
        try:
            vg = UUID(g)
        except ValueError as e:
            vg = uuid4()
        return str(vg)
            
    @classmethod
    def from_dbstream_image(cls, db_json: Dict):
        """ this factory method parses raw dyanamodb json in python dict form 
            and generates a well formed model from it.

        Args:
            db_json (Dict): The dynamodb json format in a python dict: {key: { type: value}}

        Returns:
            [type]: [description]
        """
        data = json_util.loads(db_json)
        return cls(**data)
         


class ModelError(BaseModel):
    ''' Class for IETF RFC error schema,
        we use this to return errors in the response
        
        Attributes:
            type (str): A URI identifier that categorizes the error
            title (str): A brief, human-readable message about the error
            status (str): The HTTP response code (optional)
            detail (str): A human-readable explanation of the error
            instance (str): A URI that identifies the specific occurrence of the error
    '''
    type: str = ""
    title: str = ""
    status: int = 400
    detail: str = ""
    instance: str = ""

class ResponseBody(BaseModel):
    '''Class for body of http response payload 
        Includes a list of errors if any are generated
        and a list of models that have been affected

        Attributes:
            errors (list): of ModelErrors encounterd
            models (list): of models returned
    '''
    errors: List[ModelError] = Field(default_factory=list)
    models: List[Model] = Field(default_factory=list)

class Response(BaseModel):
    ''' Response encapsulates a full response payload
        from a lambda call for v2 of the payload format
        The body of the payload is a ResponseBody object

        Attributes:
            statusCode (int): http response code
            headers (dict): dictionary of http headers, defaults with 'Content-Type': 'application/json'
            isBase64Encoded: (bool): default is false
            cookies (list): list http cookies
            body (ResponseBody): makes up the body of the response
    '''
    statusCode: int = 200
    headers: dict = {"Content-Type": "application/json"}
    isBase64Encoded: bool = False
    cookies: list = []
    body: ResponseBody = Field(default_factory=ResponseBody)

    def add_model(self, model: Model):
        self.body.models.append(model)

    def add_models(self, models: List[Model]):
        self.body.models.extend(models)

    def add_boto_error(self, error: ClientError):
        err = ModelError()
        # make err out of error
        err.title = error.response['Error']['Code']
        err.detail = error.response['Error']['Message']
        err.status = error.response['ResponseMetadata']['HTTPStatusCode']
        self.body.errors.append(err)
        self.statusCode = err.status
    
    def add_model_error(self, error: ModelError):
        self.statusCode = error.status
        self.body.errors.append(error)

    def dump(self) -> Dict:
        '''
            This creates a properly formatted response dictionary to return
            from a lambda handler call
        '''
        me = self.dict(exclude={'body'})
        me['body']=''
        if self.body is not None:
            me['body'] = self.body.json()
        return me

class ModelStore():
    """ ModelStore class encapsulates the persistence layer functions 
        for the 'Model' in a dynamodb table
    """
    def __init__(self, table_name: str = 'models', region: str= "us-east-1") -> None:
        self.region = region
        self.table_name = table_name
        self.conn=None
        self.table=None
        try:
            self._connect(table_name, region)
        except:
            pass
        self.logger =  Logger(child=True)


    def _connect(self, table_name: str = 'models', region: str= "us-east-1") -> None:
        self.conn = boto3.resource('dynamodb', region_name=region)
        self.table = self.conn.Table(table_name)

    def post(self, model: Model, query_params: dict) -> Response:
        response = Response()
        item=model.dict(exclude_defaults=True)
        try:
            resp = self.table.put_item(
                Item=item,
                ConditionExpression=Attr('guid').not_exists()
            )
        except ClientError as e:
            self.logger.error(e)
            response.add_boto_error(e)
        else:
            response.add_model(model)
        return response

    def get(self, model: Model, query_params: dict) -> Response:
        guid = str(model.guid)
        response = Response()
        try:
            items = self.table.get_item(Key={"guid": guid})
        except ClientError as e:
            self.logger.error(e.response['Error']['Message'])
            response.add_boto_error(e)
        else:
            item = items.get('Item', None)
            if item is not None:
                response.add_model(Model(**item))
            else:
                m = ModelError(status=400, title="object not found", detail=f"Object with guid: {guid} was not found")
                response.add_model_error(m)
        return response

    def get_all(self, query_params: dict = None) -> Response:
        done = False
        start_key = None
        models = list()
        response = Response()
        while not done:
            scan_kwargs = {}
            if start_key:
                scan_kwargs['ExlusiveStartKey']=start_key
            try:
                resp = self.table.scan(**scan_kwargs)
            except ClientError as e:
                self.logger.error(e.response['Error']['Message'])
                response.add_boto_error(e)
            else:
                for item in resp.get('Items', []):
                    models.append(Model(**item))
                start_key = resp.get('LastEvaluatedKey', None)
                done = start_key is None
        response.add_models(models)
        return response
    
    def patch(self, model: Model, query_params: dict) -> Response:
        response = Response()
        item=model.dict(exclude_defaults=True)
        try:
            resp = self.table.put_item(
                Item=item,
                ConditionExpression =Attr("guid").eq(model.guid),
                ReturnValues = "ALL_OLD"
            )
        except ClientError as e:
            self.logger.error(e)
            response.add_boto_error(e)
        else:
            attr = resp.get("Attributes", None)
            if attr:
                old_model = Model(**attr)
                response.add_model(old_model)        
            response.add_model(model)
        return response

    def delete(self, model: Model, query_params: dict) -> Response:
        response = Response()
        key = { 'guid' : model.guid }
        try:
            resp = self.table.delete_item(
                Key=key,
                ConditionExpression =Attr("guid").eq(model.guid),
                ReturnValues="ALL_OLD"
            )
        except ClientError as e:
            self.logger.error(e)
            response.add_boto_error(e)
        else:
            attr = resp.get("Attributes", None)
            if attr:
                model = Model(**attr)
                response.add_model(model)
        return response

class ModelEventDetail(BaseModel):
    """ ModelEventDetail class is a data structure consumed by 
        ModelChangeEvent. When serialized it comprises the 
        detail field of an eventbridge event

        Attributes:
            model_id (str): the uuid for the model
            event_type (str): unique identifier for event
            old_model: (Model): (Optional) may be present if a change or deletion has occured
            new_model: (Model): (Optional) may be present if a change or creation has occured
    """
    model_id: str = ""
    event_type: str = ""
    old_model: Optional[Model] = None
    new_model: Optional[Model] = None


class ModelChangeEvent(BaseModel):
    """ ModelChangeEvent class encapsulates the data structure and functionality for
        a Model change event generated by dynamodb streams. 
        Using the send event a instance will be put to an eventbridge client. 
        
    Attributes:
        Source: (str): [description]
        EventBusName: (str): (Optional) if not specified event is sent to default
        Resources: (list[str]): (Optional) 
        DetailType: (str): the identifier of the type of detail 
        Detail: (ModelEventDetail): the data passed from dynamodb streams
    """

    Source: str = None
    EventBusName: Optional[str] = None
    Resources: Optional[List[str]] = None
    DetailType: str
    Detail: ModelEventDetail
   
    def send(self, eventbridge: boto3.client):
        """Send takes boto client connection to eventbridge
            and executes a put_event for the serialized version of this object

        Args:
            eventbridge (boto3.client): the provisioned boto3 client ('events')

        Returns:
            result [dict]: the boto3 response from the api call put_event
        """
        result = eventbridge.put_events(Entries=[self.dump()])
        return result

    def dump(self) -> Dict:
        """ This creates a properly formatted response dictionary to return
            from a lambda handler call
       """
        me = self.dict(exclude={'Detail'}, exclude_unset=True)
        me['Detail']=''
        if self.Detail is not None:
            me['Detail'] = self.Detail.json()
        return me

    @classmethod
    def from_dynamodb_record(cls, event_type: str, record: DynamoDBStreamRecordModel):
        """ Factory classmethod to generate a well-formed ModelChangeEvent 
            from an incoming dynamodb stream event.

        Args:
            event_type (str): Identifier for event type being transcribed
            record (DynamoDBStreamRecordModel): incoming event from dynamodb stream

        Returns:
            [ModelChangeEvent]: Instance of ModelChangeEvent
        """
        old_model = None
        new_model = None

        if record.dynamodb.OldImage is not None:
            old_model = Model.from_dbstream_image(record.dynamodb.OldImage)
    
        if record.dynamodb.NewImage is not None:
            new_model = Model.from_dbstream_image(record.dynamodb.NewImage)

        model_id = json_util.loads(record.dynamodb.Keys)['guid']

        evtd = ModelEventDetail(
            event_type = event_type,
            old_model = old_model,
            new_model = new_model,
            model_id = model_id
        )
        evt = cls(
            Source ="model.api.events",
            DetailType = f"model.change.{event_type.lower()}",
            Detail = evtd
        )
        return evt  