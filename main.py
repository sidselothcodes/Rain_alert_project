import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "AC4d8a205269c0fa3e0c64c1ed411d5a4e"
auth_token = os.environ.get("AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("twilio_number")
MY_NUMBER = os.environ.get("number")

weather_params = {
    "lat": 40.495949,
    "lon": -74.444122,
    "appid": api_key,
    "exclude": "current, minutely, daily"
}
response = requests.get(OWM_Endpoint, params=weather_params)
weather_data = response.json()
hourly_data = weather_data["hourly"][:13]
will_rain = False

for data in hourly_data:
    condition_code = (data["weather"][0]["id"])
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to carry an umbrella☔️",
        from_= TWILIO_NUMBER ,
        to= MY_NUMBER
    )
    print(message.status)
