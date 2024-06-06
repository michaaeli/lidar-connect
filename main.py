import json
import requests

class Server():
    def __init__(self, url):
        self.url = url
        self.check_status()

    def check_status(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 201:
                print("Server is up.")
                return True
        except:
            raise Exception("Make sure everything is running")

    def send_objects(self, data):
        res = requests.post(url=url, json=data)
        print(res.text)

url = 'http://localhost:3000/cars'

data = {
    "make" : "Mercedes",
    "color" : "Silver",
    "price" : 75000
}

car = Server(url)
car.send_objects(data)

#class Server(url):
    #if(url)

    # on init check url
    # keep server url
    # send_objects([...])
        # post_to_server(...)


