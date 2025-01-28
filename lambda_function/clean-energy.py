import requests
import boto3
import datetime
import json
from botocore.exceptions import ClientError
from datetime import datetime



def get_secret():
    secret_name = "clean-energy-secrets"
    region_name = 'us-east-1'

    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        return secret 
    except ClientError as e:
        raise Exception(f"Error retrieving secret: {e}")


def lambda_handler(event, context):
    try:
        secrets = get_secret()
        api_key = secrets.get('OPENWEATHER_API_KEY')
        if not api_key:
            raise Exception("secret not found in secrets")

        #city = event['queryStringParameters']['city'] if event['queryStringParameters'] else 'New York'
        city = event.get('city', 'New York') 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        # Make the API request
        response = requests.get(url)
        response.raise_for_status()

        weather_data = response.json()

        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        transformed_data = {
            'city': city,
            'temperature': temperature,
            'weather_description': weather_description,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'timestamp': datetime.now().isoformat()
        }

        # Step 7: Store the data in S3
        s3 = boto3.client('s3')
        bucket_name = 'clean-energy-bucket'
        file_key = f'weather-data/{city}/{city}.json'

        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(transformed_data)
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data stored in S3 successfully',
                's3_location': f's3://{bucket_name}/{file_key}'
            })
        }

    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }