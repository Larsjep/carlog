import boto3
import requests
import json
import time
from decimal import Decimal
from os import environ

print("Hi")


ACCESS_ID = "AKIAIL724KEBU5AQFHYQ"
ACCESS_KEY  = environ['ACCESS_KEY']

# client = boto3.client('dynamodb')

dynamodb = boto3.resource(
    'dynamodb',
    region_name='eu-north-1',
    aws_access_key_id=ACCESS_ID,
    aws_secret_access_key= ACCESS_KEY
    )

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

table = dynamodb.Table('Autolog')

response = table.put_item(
   Item={
        'Lognumber' : int(1),
        'date': Decimal(time.time()),
        'positions': [Decimal(x) for x in [1,2,3,4]]
        }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4))

response = table.get_item(
    Key={ 'Lognumber' : int(1) }
)

print("GutItem succeeded:")
print(json.dumps(response, indent=4, cls=DecimalEncoder))

print("Done :)")