from collections import deque


class RingBuffer:

    def __init__(self, max_size=60):
        self.buffer = deque(maxlen=max_size)

    def append(self, item):
        self.buffer.append(item)

    def get_all(self):
        return list(self.buffer)

    def clear(self):
        self.buffer.clear()

    def __len__(self):
        return len(self.buffer)