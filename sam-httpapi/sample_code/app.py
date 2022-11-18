import os
import json
from typing import Any, Dict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver


logger = Logger()
app = APIGatewayHttpResolver()

API_VERSION = os.environ["API_VERSION"]

# GET(path parameter なし)の例
@app.get(f"/{API_VERSION}/sample/hello")
def get_sample1():

    response_body = {
        "statusCode": 200,
        "data": {
            "message": "Hello World!"
            }
        }        
    return response_body

# GET(path parameter あり)の例
@app.get(f"/{API_VERSION}/sample/names/<name>")
def get_sample2(name:str):

    # DB接続異常などの時は、以下のようにして、500 を返す
    # raise NotFoundError()

    response_body = {
        "statusCode": 200,
        "data": {
            "success": True,
            "name": name
            }
        }        
    return response_body



# POST(path parameter あり)の例
@app.post(f"/{API_VERSION}/sample/ids/<id>")
def post_sample1(id:str):
    # なにか更新する処理など

    # id > 999は存在しないとして、指定のidが存在しない時、以下のようにraise NotFoundErrorを呼ぶ
    if int(id) > 999:
        raise NotFoundError("Unsent Data for the specified ID does not exist.")
    else:
        response_body = {
            "statusCode": 200,
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
        return "Not found"

class InternalServerError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Internal Server Error"

@logger.inject_lambda_context(log_event=True) 
def lambda_handler(event: APIGatewayProxyEventV2, context: LambdaContext) -> Dict[str, Any]:

    try:
        logger.info(json.dumps(event, ensure_ascii=False, indent=2))

        return app.resolve(event, context)


    except NotFoundError as e:
        logger.exception(e)
        return {
            "statusCode": 404,
            "body": json.dumps({
                "statusCode": 404,
                "message": "Not found",
                "detail": e.msg
            })
        }        

    except InternalServerError as e:
        logger.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "message": "Internal Server Error"
            })
        }
