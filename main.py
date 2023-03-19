import requests
import time
import smtplib
from datetime import datetime


MY_LAT = 43.759838 # Your latitude
MY_LONG = -79.411209 # Your longitude

MY_EMAIL = ""
PASSWORD = ""
On_mode = True

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (iss_latitude <= MY_LAT + 10 and iss_longitude >= MY_LAT - 10) and (iss_longitude <= MY_LONG + 10 and iss_longitude >= MY_LONG - 10):
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True



while(On_mode):

    time.sleep(60)

    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL,password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="",
                msg="Subject:Hey ISS is right above us!\n\n The ISS is above us "
            )
    else:
        pass




