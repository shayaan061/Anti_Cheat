from app.utils.ring_buffer import RingBuffer

buffer = RingBuffer(max_size=3)

buffer.append(1)
buffer.append(2)
buffer.append(3)

print(buffer.get_all())

buffer.append(4)

print(buffer.get_all())