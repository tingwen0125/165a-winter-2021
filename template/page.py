from template.config import *

'''The Page class provides low-level physical storage capabilities. In the provided
skeleton, each page has a fixed size of 4096KB. This should provide optimal
performance when persisting to disk as most hard drives have blocks of the same size.
You can experiment with different sizes. This class is mostly used internally by the
Table class to store and retrieve records. While working with this class keep in mind
that tail and base pages should be identical from the hardware’s point of view.
If your table has 3 columns, you would have a set of base pages containing 3 pages, 1 for each column.

Each column has a physical page, and a base page is a set of such physical pages
each column could have multiple page objects Within the same page range
'''

class Page:

    def __init__(self):
        self.num_records = 0
        self.data = bytearray(4096)  #creates an array of that size and initialized with null bytes.

    def has_capacity(self):
        if self.num_records < MAX_NUM_RECORD:  #not sure what about at the begining when we first initialize a page. 
            return True 
        else:
            return False

    def write(self, value):  #what is value?
        start=self.num_records*8
        end=(self.num_records+1)*8
        self.data[start:end]=value.to_bytes(8,'big')
        self.num_records += 1
        
class BasePage:
    
    def __init__(self, num_columns):
        self.basePage = []
        self.num_columns = num_columns
        for i in range(4 + self.num_columns):
            self.basePage.append(Page())
            
    def has_capacity(self):
        return self.basePage[0].has_capacity()

class TailPage:
    def __init__(self, num_columns):
        self.tailPage = []
        self.num_columns = num_columns
        for i in range(4 + self.num_columns):
            self.tailPage.append(Page())
            
    def has_capacity(self):
        return self.tailPage[0].has_capacity() #check if column 0 has capacity

class PageRange:
    
    def __init__(self, num_columns):
        self.num_columns = num_columns
        self.basePageList = [BasePage(self.num_columns)]
        self.tailPageList = [TailPage(self.num_columns)]
        
    def has_capacity(self):
        return len(self.basePageList) < 16 | self.basePageList[-1].has_capacity()
    
    def tailPage_has_capacity(self):
        return self.tailPageList[-1].has_capacity()
        
        
        

