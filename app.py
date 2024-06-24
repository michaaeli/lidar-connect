from receiver import Receiver, Data
from conversion import ConvertObject
from main import Server
from read_config import Config
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
        config = Config()
        lidar_coord = config.get_lidar_pos()
        self.lat1 = lidar_coord[0] #temp coords
        self.lon1 = lidar_coord[1]
        self.lat2 = lidar_coord[2]
        self.lon2 = lidar_coord[3]
        self.coordinate_converter = ConvertObject(self.logger, self.lat1, self.lon1, self.lat2, self.lon2)
        #receiver
        self.data_source = Data()
        self.converter = self.coordinate_converter
        self.result_queue = []
        self.data_receiever = Receiver(self.logger, self.data_source, self.converter, self.result_queue)
        #main/server
        self.url = Config() #temp url
        self.backend_connection = Server(self.logger, self.url.get_connection())

if __name__ == "__main__":
    app = Application()