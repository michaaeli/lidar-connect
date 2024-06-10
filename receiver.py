class Receiver():
    def __init__(self, data_source, converter, result_queue):
        self.data_source = data_source
        self.converter = converter
        self.results_queue = result_queue

    def get_data():
        