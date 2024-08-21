import queue


class Producer:
    # TODO IMPLEMENT
    def __init__(self, url: str, queue: queue.Queue) -> None:
        self.url = url
        self.q = queue

    def isalive(self) -> bool:
        return False

    def start(self) -> None:
        return NotImplemented
