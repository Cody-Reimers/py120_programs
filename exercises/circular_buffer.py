
class CircularBuffer:
    def __init__(self, number_of_slots):
        self._number_of_slots = number_of_slots
        self._slots = { number + 1: None for number in range(number_of_slots) }
        self.oldest = 1
        self.newest = 1

    @property
    def oldest(self):
        return self._oldest

    @property
    def newest(self):
        return self._newest

    @property
    def number_of_slots(self):
        return self._number_of_slots

    @property
    def slots(self):
        return self._slots

    @oldest.setter
    def oldest(self, new):
        self._oldest = new

    @newest.setter
    def newest(self, new):
        self._newest = new

    def get(self):
        slots = self.slots
        index = self.oldest
        value = slots[index]

        if value is not None:
            slots[index] = None
            self.oldest = index % self.number_of_slots + 1

        return value

    def put(self, new):
        slots = self.slots
        index = self.newest

        if slots[index] is not None:
            old_index = self.oldest
            self.oldest = old_index % self.number_of_slots + 1

        slots[index] = new
        self.newest = index % self.number_of_slots + 1

###############################################################################

buffer = CircularBuffer(3)

print(buffer.get() is None)          # True

buffer.put(1)
buffer.put(2)
print(buffer.get() == 1)             # True

buffer.put(3)
buffer.put(4)
print(buffer.get() == 2)             # True

buffer.put(5)
buffer.put(6)
buffer.put(7)
print(buffer.get() == 5)             # True
print(buffer.get() == 6)             # True
print(buffer.get() == 7)             # True
print(buffer.get() is None)          # True

buffer2 = CircularBuffer(4)

print(buffer2.get() is None)         # True

buffer2.put(1)
buffer2.put(2)
print(buffer2.get() == 1)            # True

buffer2.put(3)
buffer2.put(4)
print(buffer2.get() == 2)            # True

buffer2.put(5)
buffer2.put(6)
buffer2.put(7)
print(buffer2.get() == 4)            # True
print(buffer2.get() == 5)            # True
print(buffer2.get() == 6)            # True
print(buffer2.get() == 7)            # True
print(buffer2.get() is None)         # True
