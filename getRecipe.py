import json
import logging
import boto3
import os
import uuid
from decimal import Decimal
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

log = logging.getLogger()
log.setLevel(logging.DEBUG)

region = os.environ["AWS_REGION"]

dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('RecipeTable')

def get_from_dynamo(event):
    log.debug("Received in get_from_dynamo: {}".format(json.dumps(event)))
    RecipeName = event['pathParameters']['RecipeName']    
    log.debug("RecipeName: {}".format(RecipeName))
    item = table.get_item(
        Key={
            'RecipeName' : RecipeName
        }
    )
    log.debug(RecipeName)
    log.debug("======")
    log.debug(item)
    log.debug(event)
    log.debug(event['pathParameters'])
    return item["Item"]


def get_recipe(event, context):
    print(event)
    log.debug("Received event in get_item: {}".format(json.dumps(event)))
    body = {
        "Item": get_from_dynamo(event),
    }
    response = {
        "statusCode": 200,
        'headers': { 'Content-Type': 'application/json' },
        "body": json.dumps(body, cls=DecimalEncoder)
    }
    print("here\n\n\n")
    log.debug(response)
    return response
