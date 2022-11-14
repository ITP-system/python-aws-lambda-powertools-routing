import json
from typing import Any, Dict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver

logger = Logger()
app = APIGatewayHttpResolver()

# GET(path parameter なし)の例
@app.get("/sample/hello")
def get_sample1():
    response_body = {
        "message": "Hello World!"
        }
    return response_body

# GET(path parameter あり)の例
@app.get("/sample/names/<name>")
def get_sample2(name:str):

    response_body = {
            "success": True,
            "name": name
        }
    return response_body

# POST(path parameter あり)の例
@app.post("/sample/ids/<id>")
def post_sample1(id:int):

    # なにか更新する処理

    response_body = {
        "data": {
            "success": True,
            "id": id
            }
        }
    return response_body

class NotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "NOT_FOUND"

class InternalServerError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "INTERNAL_SERVER_ERROR"

@logger.inject_lambda_context(log_event=True) 
def lambda_handler(event: APIGatewayProxyEventV2, context: LambdaContext) -> Dict[str, Any]:

    try:
        logger.info(json.dumps(event, ensure_ascii=False, indent=2))

        return app.resolve(event, context)


    except NotFoundError as e:
        print("error")
        print(e)
        return {
            "statusCode": 404,
            "body": json.dumps({
                "success": False,
                "meta": {
                "code": 404,
                "message": "NOT_FOUND",
                "detail": e.msg
                }
            })
        }

    except InternalServerError as e:
        print("error")
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "meta": {
                "code": 500,
                "message": e.msg
                }
            })
        }