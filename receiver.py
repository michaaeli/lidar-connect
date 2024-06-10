from conversion import ConvertObject

class Receiver():
    def __init__(self, data_source, converter, result_queue):
        self.data_source = data_source
        self.converter = converter
        self.result_queue = result_queue

    def convert(self):
        # self.data_source = Data()
        # data_to_convert = self.data_source.get_data()
        #test code
        data_to_convert = self.data_source
        result = self.converter.get_final_coords(-1142.63, 1110.45)
        return result
    
    def enqueue(self):
        self.result_queue.append(self.convert())
        return self.result_queue
    
class Data():
    def __init__(self) -> None:
        pass

    def get_data(self):
        x = 0
        y = 1
        z = 2
        return [x, y, z]

# test 3
# x = getLLH(33.730979, -117.937358, 33.736142, -117.943838, -1142.63, 1110.45)
# Expected 33.737889, -117.946033
# Actual   33.730433665414175, -117.95457518440682

data1 = (33.730979, -117.937358, 33.736142, -117.943838)
arr = []
i = ConvertObject(33.730979, -117.937358, 33.736142, -117.943838)

x = Receiver(data1, i, arr)
print(x.convert())
print(x.enqueue())

