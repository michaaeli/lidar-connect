from receiver import Receiver, Data
from conversion import ConvertObject
from main import Server

class Application():
    def __init__(self):
        #receiver
        self.data_source = Data()
        self.converter = self.data_source.convert()
        self.result_queue = self.converter.enqueue()
        self.data_receiever = Receiver(self.data_source, self.converter, self.result_queue)
        #conversion
        self.lat1 = 1  #temp coords
        self.lon1 = 1
        self.lat2 = 2
        self.lon2 = 2
        self.coordinate_converter = ConvertObject(self.lat1, self.lon1, self.lat2, self.lon2)
        #main/server
        self.url = 'http://localhost:3000/cars' #temp url
        self.backend_connection = Server(self.url)
    