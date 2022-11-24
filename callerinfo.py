import phonenumbers
import folium
from phonenumbers import carrier, geocoder, timezone
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
import time
from sinchsms import SinchSMS


mobileNo = input("Enter Mobile Number with country code: ")
Mobile = str(mobileNo[3:])
mobileNo = phonenumbers.parse(mobileNo)

possibility = phonenumbers.is_possible_number(mobileNo)
print("Checking posssibility of a Number:", possibility)

Valid = phonenumbers.is_valid_number(mobileNo)
print("Valid Mobile Number :", Valid)

timeZone = timezone.time_zones_for_number(mobileNo)
print(timeZone)

service_pro = mobileNo
print("The Service Provider for the input number is", carrier.name_for_number(service_pro, 'en'))

location = geocoder.description_for_number(mobileNo, "en")
print(location)

from opencage.geocoder import OpenCageGeocode
key = '193e60ed59f5435ea9783c15c65a8506'

geocoder = OpenCageGeocode(key)
query = str(location)
results = geocoder.geocode(query)


lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']

print("The latitude is: {} The longitude is: {}".format(lat, lng))

myMap = folium.Map(location=[lat, lng], zoom_start=9)
folium.Marker([lat, lng], popup=location).add_to(myMap)

myMap.save("mylocation.html")

def sendSMS():

	number = 'Clients_mobile_number'
	app_key = 'Clients_app_key'
	app_secret = 'Clients_app_secret'


	message = 'Hello Message!!!'

	client = SinchSMS(app_key, app_secret)
	print("Sending '%s' to %s" % (message, number))

	response = client.send_message(number, message)
	message_id = response['messageId']
	response = client.check_status(message_id)


	while response['status'] != 'Successful':
		print(response['status'])
		time.sleep(1)
		response = client.check_status(message_id)

	print(response['status'])

root = tk.Tk()
root.geometry('500x300')
root.maxsize(500, 300)
root.minsize(500, 300)
root.title('Send SMS')
root.iconbitmap('Sms.ico')


def send_sms():
    number = phone_no.get()
    messages = message.get("1.0", "end-1c")

    url = "https://www.fast2sms.com/dev/bulk"
    api = "jf2mJKpinHOE9c6WoyetVkqauxgzS8MCBQPNFdGsv7R3rDT4lYYbpfhCu8wcdzSlmK2sXI5ZJaeky6W1"
    querystring = {"authorization": api, "sender_id": "FSTSMS", "message": messages, "language": "english",
                   "route": "p", "numbers": number}

    headers = {
        'cache-control': "no-cache"
    }
    requests.request("GET", url, headers=headers, params=querystring)
    messagebox.showinfo("Send SMS", 'SMS has been send successfully')


img = ImageTk.PhotoImage(Image.open('background.jpg'))
panel = Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

label = Label(root, text="Send SMS Using Python", font=('verdana', 10, 'bold'))
label.place(x=210, y=10)

phone_no = Entry(root, width=20, borderwidth=0, font=('verdana', 10, 'bold'))
phone_no.place(x=220, y=115)
phone_no.insert('end', '{}' .format(Mobile))

message = Text(root, height=5, width=25, borderwidth=0, font=('verdana', 10, 'bold'))
message.place(x=190, y=140)
message.insert('end', 'Checking posssibility of a Number: {0} \nValid Mobile Number :{1} \n{2} \nThe Service Provider for the input number is {3} \nCountry:{4} ' .format(possibility, Valid, timeZone, carrier.name_for_number(service_pro, 'en'), location))

send = Button(root, text="Send Message", font=('verdana', 10, 'bold'), relief=RIDGE, cursor='hand2', borderwidth=0,
              command=send_sms)
send.place(x=260, y=235)
root.mainloop()
