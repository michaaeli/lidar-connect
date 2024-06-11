from receiver import Receiver, Data
from conversion import ConvertObject
from main import Server
import logging

class Application():
    def __init__(self):
        #logger
        logging.basicConfig( level=logging.INFO, filename='app.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger('test')
        self.logger.debug('debug message')
        self.logger.info('info message')
        #conversion
        self.lat1 = 1  #temp coords
        self.lon1 = 1
        self.lat2 = 2
        self.lon2 = 2
        self.coordinate_converter = ConvertObject(self.logger, self.lat1, self.lon1, self.lat2, self.lon2)
        #receiver
        self.data_source = Data()
        self.converter = self.coordinate_converter
        self.result_queue = []
        self.data_receiever = Receiver(self.logger, self.data_source, self.converter, self.result_queue)
        #main/server
        self.url = 'http://localhost:3000/cars' #temp url
        self.backend_connection = Server(self.logger, self.url)

if __name__ == "__main__":
    app = Application()