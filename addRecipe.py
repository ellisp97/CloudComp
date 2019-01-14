import json
import logging
import boto3
import os
import uuid

log = logging.getLogger()
log.setLevel(logging.DEBUG)

region = os.environ["AWS_REGION"]

dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('RecipeTable')

def put_to_dynamo(event):
    log.debug("Received in put_to_dynamo: {}".format(json.dumps(event)))
    RecipeName = event["RecipeName"]
    Ingredients = event["Ingredients"]
    Method = event["Method"]
    RecipeTime = event["RecipeTime"]    
 
    
    table.put_item(
        Item={
            'RecipeName': RecipeName,
            'Ingredients': Ingredients,
            'Method': Method,
            'RecipeTime': RecipeTime
        }
    )
    return {RecipeName, Ingredients, Method, RecipeTime}
    
    
def create_recipe(event, context):
    log.debug("Event in create_item: {}".format(json.dumps(event)))
    RecipeName, Ingredients, Method, RecipeTime = put_to_dynamo(event)
    body = {
        "RecipeName": " {}".format(RecipeName),
        "Ingredients": " {}".format(Ingredients),
        "Method": " {}".format(Method),
        "RecipeTime": " {}".format(RecipeTime),
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
