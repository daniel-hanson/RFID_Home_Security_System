# Download the Python helper library from twilio.com/docs/python/install
# pip3 install twilio
# pip3 install pyimgur
from twilio.rest import Client
import pyimgur
import time

CLIENT_ID = "10b403a3155f56f"
PATH = 'C:\\Users\\dhans\\Pictures\\Hanson_Daniel_May22.jpg' # Local image path goes here
sendingPhone = "+19132701092"
receivingPhone = "+18167286516"

def triggerAlertSystem():
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.size)
    print(uploaded_image.type)

    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACb7afcb9e77c9f887cf2ef49236f502f4"
    auth_token = "e31dadfb68e1b61895e14e8d68590710"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
            receivingPhone,
            body="",
            from_=sendingPhone,
            media_url=uploaded_image.link)

    print(message.sid)

    currentTime = time.strftime("%H:%M:%S")
    currentDate = time.strftime("%m/%d/%Y")
    textBody = "Door alarm triggered at: " + currentTime + " on " + currentDate

    message2 = client.messages.create(
            receivingPhone,
            body=textBody,
            from_=sendingPhone)

    print(message2.sid)


triggerAlertSystem()
