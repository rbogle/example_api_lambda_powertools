from aws_cdk import core
from aws_cdk import aws_dynamodb as ddb
from aws_cdk import aws_lambda
from aws_cdk import aws_apigatewayv2 as apigw2
from aws_cdk import aws_apigatewayv2_integrations as apigw2_int
import os


class InfraStack(core.Stack):

    def __init__(self, scope: core.Construct, stack_name: str, **kwargs) -> None:
        super().__init__(scope, stack_name, **kwargs)

        '''
            we create 
                dynamodb table with a primary key
                a lambda layer with the import requirements for the lambda
                a lambda to handle api requests
                a  http api gateway v2
                and a route to handle any method and all requests to /api
        '''
            
        layer_name = os.getenv("LAYER_NAME")
        layer_version = os.getenv("LAYER_VERSION")
        layer_path = f"layers/{layer_name}_{layer_version}.zip"

        # dynamodb table with a id partition key
        ddb_table  = ddb.Table(
            self, 
            f"{stack_name}-ddb-table",
            partition_key=ddb.Attribute(
                name='guid', 
                type=ddb.AttributeType.STRING
            )
        )

        # create a layer for the lambda required imports
        fn_layer = aws_lambda.LayerVersion(
            self,
            f"{stack_name}-lambda-layer",
            layer_version_name=f"{stack_name}-{layer_name}",
            code = aws_lambda.Code.from_asset(layer_path),
        )

        # create api lambda
        api_lambda = aws_lambda.Function(
            self, 
            f"{stack_name}-api-fn",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            handler="api.router",
            code=aws_lambda.Code.from_asset("src"),
            timeout=core.Duration.seconds(30),
            layers=[fn_layer],
            environment = {
                "DDB_TABLE_NAME":ddb_table.table_name
            }
        )

        # create http api-gw
        http_api = apigw2.HttpApi(
            self,
            f"{stack_name}-api-gw",
            create_default_stage = True
        )

        # allow lambda to write to ddb        
        ddb_table.grant_read_write_data(api_lambda)

        # create lambda integration and configure route
        api_integration = apigw2_int.LambdaProxyIntegration(handler=api_lambda)

        # add proxy any route to http api gw
        http_api.add_routes(
            path="/api/{proxy+}",
            methods=[apigw2.HttpMethod.ANY],
            integration=api_integration
        )

        core.CfnOutput(self, "Api", value=http_api.url, description="URL of the API Gateway")
        core.CfnOutput(self, "DynamoDB_Name", value=ddb_table.table_name, description="DynamoDB Table Name")
        core.CfnOutput(self, "DynamoDB_ARN", value=ddb_table.table_arn, description="DynamoDB Table ARN")