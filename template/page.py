from template.config import *

'''The Page class provides low-level physical storage capabilities. In the provided
skeleton, each page has a fixed size of 4096KB. This should provide optimal
performance when persisting to disk as most hard drives have blocks of the same size.
You can experiment with different sizes. This class is mostly used internally by the
Table class to store and retrieve records. While working with this class keep in mind
that tail and base pages should be identical from the hardware’s point of view.
'''

class Page:

    def __init__(self):
        self.num_records = 0
        self.data = bytearray(4096)

    def has_capacity(self):
        pass

    def write(self, value):
        self.num_records += 1
        pass

