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


secrets = get_secret()
weather_api_key = secrets.get('OPENWEATHER_API_KEY')
nrel_api_key = secrets.get("NREL_API_KEY")

VALID_CITIES = {
    'New York': {
        'lat': 40.7128,
        'lon': -74.0060,
        'state': 'NY'
    },
    'Boston': {
        'lat': 42.3601,
        'lon': -71.0589,
        'state': 'MA'
    },
    'Hartford': {
        'lat': 41.7658,
        'lon': -72.6734,
        'state': 'CT'
    },
    'Philadelphia': {
        'lat': 39.9525,
        'lon': -75.1652,
        'state': 'PA'
    },
    'Washington, D.C.': {
        'lat': 38.9072,
        'lon': -77.0369,
        'state': 'DC'
    },
    'Miami': {
        'lat': 25.7617,
        'lon': -80.1918,
        'state': 'FL'
    },
    'Atlanta': {
        'lat': 33.7490,
        'lon': -84.3880,
        'state': 'GA'
    },
    'Charlotte': {
        'lat': 35.2271,
        'lon': -80.8431,
        'state': 'NC'
    },
    'Baltimore': {
        'lat': 39.2904,
        'lon': -76.6122,
        'state': 'MD'
    }
}


def lambda_handler(event, context):

    city = event.get('queryStringParameters', {}).get('city', 'New York')

    if not city or city not in VALID_CITIES:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Invalid city selection'})
        }
    
    try:
        city_data = VALID_CITIES[city]
        lat = city_data['lat']
        lon = city_data['lon']

        weather = get_openweather_data(city, city_data['state'])

        temperature = weather['main']['temp']
        weather_description = weather['weather'][0]['description']
        humidity = weather['main']['humidity']
        wind_speed = weather['wind']['speed']

        transformed_data = {
        'city': city,
        'temperature': temperature,
        'weather_description': weather_description,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'timestamp': datetime.now().isoformat()
        }

        s3 = boto3.client('s3')
        bucket_name = 'clean-energy-bucket'
        file_key = f'weather-data/{city}/{city}.json'

        s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=json.dumps(transformed_data)
        )


        # Get energy estimation
        energy = {
            'solar': get_pvwatts_estimate(lat, lon)
        }
        
        return success_response({
            'weather': transformed_data,
            'energy': energy
        })
        
    except Exception as e:
        return error_response(str(e), 500)



def get_openweather_data(city: str, state: str) -> dict:
    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': f"{city},{state},US",
        'appid': weather_api_key,
        'units': 'imperial'
    }

    response = requests.get(weather_url, params=params)
    response.raise_for_status()
    return response.json()



def get_pvwatts_estimate(lat: float, lon: float) -> dict:
    url = "https://developer.nrel.gov/api/pvwatts/v6.json"
    params = {
        'api_key': nrel_api_key,
        'lat': round(lat, 4),  
        'lon': round(lon, 4),
        'system_capacity': 4,
        'azimuth': 180,
        'tilt': 30,  
        'array_type': 1,
        'module_type': 0,
        'losses': 14,
        'timeframe': 'hourly'
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['outputs']


def success_response(data: dict) -> dict:
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }

def error_response(message: str, code: int) -> dict:
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': message})
    }

