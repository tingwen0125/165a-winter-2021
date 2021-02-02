from template.page import *
from template.index import Index
from time import time

INDIRECTION_COLUMN = 0
RID_COLUMN = 1
TIMESTAMP_COLUMN = 2
SCHEMA_ENCODING_COLUMN = 3

'''
The Table class provides the core of our relational storage functionality. All columns are
64-bit integers in this implementation. Users mainly interact with tables through queries.
Tables provide a logical view over the actual physically stored data and mostly manage
the storage and retrieval of data. Each table is responsible for managing its pages and
requires an internal page directory that given a RID it returns the actual physical location
of the record. The table class should also manage the periodical merge of its
corresponding page ranges.
'''
#16 base pages in one page range
class Record:

    def __init__(self, rid, key, columns):
        self.rid = rid
        self.key = key
        self.columns = columns

class Table:

    """
    :param name: string         #Table name
    :param num_columns: int     #Number of Columns: all columns are integer
    :param key: int             #Index of table key in columns
    """
    def __init__(self, name, num_columns, key):
        self.name = name
        self.key = key
        self.num_columns = num_columns
        self.page_directory = {}
        self.index = Index(self)
        self.pageRanges = [PageRange(self.num_columns)]
        self.keyToBaseRID = {} 
        self.baseRID = 1
        self.tailRID = 1

        pass

    def getPageR(self,rid): #given rid return the page range the rid record is at
        return rid//MAX_NUM_RECORD//BASE_PAGE_PER_PAGE_RANGE
    def __merge(self):
        pass
