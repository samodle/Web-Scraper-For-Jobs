import boto3

def makeADynamoDBTable():
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')


    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='jobposts',
        KeySchema=[
            {
                'AttributeName': 'jobtitle',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'company',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'jobtitle',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'company',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'url',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'location',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'searchterm',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'source',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'companyrating',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'salary',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'commitment',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'description',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'datecreated',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'dateupdated',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='users')

    # Print out some data about the table.
    print(table.item_count)