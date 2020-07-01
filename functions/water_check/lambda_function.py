import os
from datetime import datetime
import requests
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
SITE = 'https://waterservices.usgs.gov/nwis/iv/?format=json&sites=02146614&parameterCd=00065'
SNS_ARN = os.environ.get('SNS_ARN')
TABLE_NAME = 'WaterLevelTable'
boot = False

def lambda_handler(event, context):
    #Load Defaults If Empty Table
    if not boot:
        bootstrap(TABLE_NAME)
    
    print('Checking Water Data')
    try:
        req = requests.get(SITE)
        jsonResponse = req.json()
        height = Decimal(jsonResponse['value']['timeSeries'][0]['values'][0]['value'][0]['value'])
        
        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={'TYPE': 'LAST'})
        last_height = response['Item']['HEIGHT']
        
        #Breach 
        response = table.get_item(Key={'TYPE': 'BREACH'})
        breach_height = response['Item']['HEIGHT']
        
        if height > last_height and last_height < breach_height and height > breach_height:
            message = f'Backyards are flooding. Water is {height} feet high.'
            send(message)
        
        if height < last_height and last_height > breach_height and height < breach_height:
            message = f'Flooding has receded. Water is {height} feet high.'
            send(message)
        
        #Flood Stage
        response = table.get_item(Key={'TYPE': 'FLOOD'})
        flood_height = response['Item']['HEIGHT']
        
        if height > last_height and last_height < flood_height and height > flood_height:
            message = f'Creek at NWS Flood Stage. Water is {height} feet high.'
            send(message)
        
        #Record
        response = table.get_item(Key={'TYPE': 'RECORD'})
        record_height = response['Item']['HEIGHT']
        
        if height > last_height and last_height < record_height and height > record_height:
            message = f'Creek at record highs. Water is {height} feet high.'
            send(message)
        
        #Update last height
        response = table.update_item(
            Key={'TYPE': 'LAST'},
            UpdateExpression="set HEIGHT=:h",
            ExpressionAttributeValues={':h': height}
        )

    except:
        print('Check Failed')
        raise

def send(msg):
    sns.publish(
            TopicArn = SNS_ARN,
            Subject = 'High Creek Warning',
            Message = msg,
            MessageAttributes = {
                'event_type': {
                    'DataType': 'String',
                    'StringValue': 'water_warning'
                }
            }
        )

def bootstrap(tablename):
    # Checks Dynamo table for valid starting entries, populates default if not found
    try:
        WaterTable = { 'LAST': 1, 'BREACH': 13, 'FLOOD': 16, 'RECORD': 20} 
        table = dynamodb.Table(tablename)
        for key, value in WaterTable.items():
            response = table.get_item(Key={'TYPE': key})
            if not 'Item' in response:
                print('Bootstrap table ' + tablename + ' with ' + key + ':' + str(value))
                response = table.update_item(
                    Key={'TYPE': key},
                    UpdateExpression="set HEIGHT=:h",
                    ExpressionAttributeValues={':h': value}
                )
        boot = True
    except:
        print('Bootstrap Operation Failed')