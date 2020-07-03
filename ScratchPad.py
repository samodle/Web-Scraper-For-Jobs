import boto3
from DynamoConfig import makeADynamoDBTable

#makeADynamoDBTable()

TABLE_NAME = "JobPost"

# Creating the DynamoDB Client
dynamodb_client = boto3.client('dynamodb')

# Creating the DynamoDB Table Resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

print(table.creation_date_time)

table.put_item(
   Item={
        'JobTitle': 'janedoe',
        'CompanyID': 255,
        'last_name': 'Doe',
       # 'age': 25,
       # 'account_type': 'standard_user',
    }
)



