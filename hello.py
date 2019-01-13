def noop(event, context):
    return {
        "body": "hello",
        "headers": {},
        "statusCode": 200
    }
