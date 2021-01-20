import sys,json

# need to patch path due to the way lambdas handle imports
libdir = f"{sys.path[0]}/src"
sys.path.insert(0,libdir)

def get_model_set() -> list:
    return [
        {
            'guid': 'b1e0e990-7ac5-4711-9a33-97d11403f7f7',
            'name': 'martha',
            'metadata' : {
                "foo": "bar"
            }
        },
        {
            'guid': '86e42e5d-7d94-4c93-b2c8-e06d1ade0f0b', 
            'name': 'abigail',
            'metadata' : {
                "foo": "baz"
            }
        },
        {
            'guid': '84de05a3-9d68-41ae-b291-1405bc902389',
            'name': 'dolley',
            'metadata' : {
                "foo": "buz"
            }
        },
    ]
def get_mock_model_unknown() -> dict:
    return {
            'guid': '00000000-0000-0000-0000-00000000000',
            'name': 'bill',
            'metadata' : {
                "foo": "apples"
            }        
    }

def get_mock_model(id=0) -> dict:
    return get_model_set()[id]

def get_known_id(id=0) -> str:
    m = get_model_set()[id]
    return m['guid']

def get_known_name(id=0) -> str:
    m = get_model_set()[id]
    return m['name']

def get_known_metadata(id=0) -> dict:
    m = get_model_set()[id]
    return m['metadata']

def api_gateway_event_v2(payload: dict, path: str="", method: str="") -> dict:
    return {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": path,
        "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
        "cookies": [
            "cookie1",
            "cookie2"
        ],
        "headers": {
            "Header1": "value1",
            "Header2": "value1,value2"
        },
        "queryStringParameters": {
            "parameter1": "value1,value2",
            "parameter2": "value"
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "api-id",
            "authentication": {
            "clientCert": {
                "clientCertPem": "CERT_CONTENT",
                "subjectDN": "www.example.com",
                "issuerDN": "Example issuer",
                "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                "validity": {
                "notBefore": "May 28 12:30:02 2019 GMT",
                "notAfter": "Aug  5 09:36:04 2021 GMT"
                }
            }
            },
            "authorizer": {
                "jwt": {
                    "claims": {
                    "claim1": "value1",
                    "claim2": "value2"
                    },
                    "scopes": [
                    "scope1",
                    "scope2"
                    ]
                }
            },
            "domainName": "id.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "id",
            "http": {
            "method": method,
            "path": path,
            "protocol": "HTTP/1.1",
            "sourceIp": "IP",
            "userAgent": "agent"
            },
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default",
            "time": "12/Mar/2020:19:03:58 +0000",
            "timeEpoch": 1583348638390
        },
        "body": json.dumps(payload),
        "pathParameters": {
            "parameter1": "value1"
        },
        "isBase64Encoded": False,
        "stageVariables": {
            "stageVariable1": "value1",
            "stageVariable2": "value2"
        }
    }