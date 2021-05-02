import os
import random
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb", region_name='eu-west-2')

ANIMALS = os.environ['ANIMALS'].split(",")

def spiritual_animal_finder(event):
    response = {
        "animal": check_user(event)
    }
    return response
    
def check_user(event):
    if "name" in event:
        user = event["name"]
    else:
        return "Bad request, no user key in the payload"    
    users = dynamodb.Table('playground-feasible-panda')
    try:
        response = users.get_item(
            Key={
                'users': user
            }
        )
        print("user", response)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response:
            return response['Item']['animals']
        else:
            animal = random.choice(ANIMALS)
            add_user(user, animal)
            return animal
            
def add_user(user,animal):
    table = dynamodb.Table('playground-feasible-panda')
    table.update_item(
        Key={
        'users': user
        
    },
    UpdateExpression="set animals = :c",
    ExpressionAttributeValues={
        ':c': animal
    },
    ReturnValues="UPDATED_NEW"
    )
    print("PutItem succeeded:")
    
def lambda_handler(event, context):
    return spiritual_animal_finder(event)