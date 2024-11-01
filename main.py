import requests, smtplib, time
from datetime import datetime

# MY_LAT = float(33.684422)  #your latitude
# MY_LONG = float(73.047882)  #your longitude

MY_LAT = 51
MY_LONG = 109


# is your position is within +5 or -5 degrees of the ISS position?
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])
    iss_position = (latitude, longitude)
    if abs(MY_LAT - latitude) <= 5 and abs(MY_LONG - longitude) <= 5:
        return True


# is it currently dark?
def is_dark():
    time_now = datetime.now()
    hour = time_now.hour

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "tzid": "Asia/Karachi",
        "formatted": 0,
    }

    time_response = requests.get(url=f"https://api.sunrise-sunset.org/json", params=parameters)
    time_data = time_response.json()
    sunrise = int(time_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(time_data["results"]["sunset"].split("T")[1].split(":")[0])

    if hour >= sunset or hour <= sunrise:
        return True


def send_email():
    my_email = "waqarpython@gmail.com"
    password = "nxbfzsvpdqtcoszr"
    content = "The ISS station is right above your location!"
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="waqarpython@yahoo.com",
            msg=f"subject: LOOK UP! 👆\n\n{content}"
        )


# if the ISS is close to my current position, and it is currently dark, then send yourself an email to look up.
# Bonus: Run the code every 60 seconds.
while is_iss_overhead() and is_dark():
    send_email()
    time.sleep(60)
