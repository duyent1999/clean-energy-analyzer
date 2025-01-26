
def get_secret():
    secret_name = "clean-energy-secrets"
    region_name = 'us-east-1'

    # Create a Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        return secret  # Return all secret values as a dictionary
    except ClientError as e:
        raise Exception(f"Error retrieving secret: {e}")


def lambda_handler(event, context):
    try:
        # Step 1: Retrieve the API key from Secrets Manager
        secrets = get_secret()
        api_key = secrets.get('OPENWEATHER_API_KEY')
        if not api_key:
            raise Exception("secret not found in secrets")

        # Step 2: Define the city and API endpoint
        city = event.get('city', 'London')  # Default to London if no city is provided
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        # Step 3: Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Step 4: Parse the JSON response
        weather_data = response.json()

        # Step 5: Extract relevant data
        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        # Step 6: Transform the data
        transformed_data = {
            'city': city,
            'temperature': temperature,
            'weather_description': weather_description,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'timestamp': datetime.utcnow().isoformat()  # Add a timestamp
        }

        # Step 7: Store the data in S3
        s3 = boto3.client('s3')
        bucket_name = 'clean-energy-bucket'  # Replace with your S3 bucket name
        file_key = f'weather-data/{city}/.json'

        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(transformed_data)
        )

        # Step 8: Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data stored in S3 successfully',
                's3_location': f's3://{bucket_name}/{file_key}'
            })
        }

    except requests.exceptions.RequestException as e:
        # Handle API request errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        # Handle other errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }