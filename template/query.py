from template.table import Table, Record
from template.index import Index
from template.page import Page, BasePage, PageRange,TailPage
import datetime
'''
The Query class provides standard SQL operations such as insert, select,
update, delete and sum. The select function returns the specified set of columns
from the record with the given key (if available). The insert function will insert a new
record in the table. All columns should be passed a non-NULL value when inserting. The
update function updates values for the specified set of columns. The delete function
will delete the record with the specified key from the table. The sum function will sum
over the values of the selected column for a range of records specified by their key
values. We query tables by direct function calls rather than parsing SQL queries.
'''

class Query:
    """
    # Creates a Query object that can perform different queries on the specified table 
    Queries that fail must return False
    Queries that succeed should return the result or True
    Any query that crashes (due to exceptions) should return False
    """

    def __init__(self, table):
        self.table = table
        pass

    """
    # internal Method
    # Read a record with specified key
    # Returns True upon succesful deletion
    # Return False if record doesn't exist or is locked due to 2PL
    """
    def delete(self, key):
        baseIndirection = self.table.BaseRIDToIndirection[self.table.keyToBaseRID[key]]
        if baseIndirection == 0:
            self.table.keyToBaseRID[key] = 0 #set baserid of the record with specified key to 0(invalid)
        else:
            t = self.table.TailRIDToIndirection
            tailIndirection = t[baseIndirection]
            while tailIndirection < 0: #while it is a tailrid
                tempTailIndirection = tailIndirection
                tailIndirection = t[tailIndirection]
                tail_rid = list(t.keys())[list(t.values()).index(tempTailIndirection)]
                tail_rid = 0
            tail_rid = list(t.keys())[list(t.values()).index(tailIndirection)] 
            tail_rid = 0
            self.table.keyToBaseRID[key] = 0

    """
    # Insert a record with specified columns
    # Return True upon succesful insertion
    # Returns False if insert fails for whatever reason
    """
    def insert(self, *columns):
        '''[0, 0, 20210131111207, 0, 906659671, 93, 0, 0, 0]'''
        total_col = []
        schema_encoding = int('0' * self.table.num_columns, 2)
        time = datetime.datetime.now()
        int_time = int(time.strftime("%Y%m%d%H%M%S"))
        curPageRange = self.table.pageRanges[-1]
        curBasePage = curPageRange.basePageList[-1]

        # open a new page range or new base page
        if curPageRange.has_capacity() == False:
            self.table.pageRanges.append(PageRange(self.table.num_columns))
            curPageRange = self.table.pageRanges[-1]
            curBasePage = curPageRange.basePageList[-1]
        elif curBasePage.has_capacity() == False:
            curPageRange.basePageList.append(BasePage(self.table.num_columns))
            curBasePage = curPageRange.basePageList[-1]
  
        total_col.extend([0, self.table.baseRID, int_time, schema_encoding])
        total_col += columns
        for i in range(len(total_col)):
            curBasePage.basePage[i].write(total_col[i])
            start = (curBasePage.basePage[i].num_records - 1) * 8
            end = curBasePage.basePage[i].num_records * 8
            #test
            int_val=int.from_bytes(curBasePage.basePage[i].data[start:end],'big')
            print(int_val)
        
        self.table.keyToBaseRID[total_col[self.table.key + 4]] = self.table.baseRID
        self.table.baseRID += 1
        return True
    
    """
    # Read a record with specified key
    # :param key: the key value to select records based on
    # :param query_columns: what columns to return. array of 1 or 0 values.
    # Returns a list of Record objects upon success
    # Returns False if record locked by TPL
    # Assume that select will never be called on a key that doesn't exist
    """
    def select(self, key, column, query_columns):

        pass

    """
    # Update a record with specified key and columns
    # Returns True if update is succesful
    # Returns False if no records exist with given key or if the target record cannot be accessed due to 2PL locking
    """
    def getUpdateRID(self,key): 
        return self.table.keyToBaseRID[key]

    def getUpdatePageR(self,rid):
        return self.table.getPageR(rid)

    def update(self, key, *columns):
        rid=self.getUpdateRID(key)
        PageR=self.getUpdatePageR(rid)
        #check if the tail page in that page range still have space
        if self.table.pageRanges[PageR].tailPage_has_capacity() == False: #if no capacity, add a new tail page
            self.table.pageRanges[PageR].tailPageList.append(TailPage(self.table.num_columns)) 
        updateEncoding=""  #updated schema encoding
        for i in range(len(columns)):
            if columns[i] == None:
                updateEncoding+"0"
            else:
                updateEncoding+"1"
        updateEncoding=int(updateEncoding)
        time = datetime.datetime.now()
        int_time = int(time.strftime("%Y%m%d%H%M%S"))
        tailrecord=[rid,self.table.tailRID,int_time,updateEncoding]+list(columns)
        currTailPage=self.table.pageRanges[PageR].tailPageList[-1]
        for i in range(len(tailrecord)):
            currTailPage.tailPage[i].write(tailrecord[i])
        self.table.tailRID +=1
        return True
        
    

    """
    :param start_range: int         # Start of the key range to aggregate 
    :param end_range: int           # End of the key range to aggregate 
    :param aggregate_columns: int  # Index of desired column to aggregate
    # this function is only called on the primary key.
    # Returns the summation of the given range upon success
    # Returns False if no record exists in the given range
    """
    def sum(self, start_range, end_range, aggregate_column_index):
        
        pass

    """
    incremenets one column of the record
    this implementation should work if your select and update queries already work
    :param key: the primary of key of the record to increment
    :param column: the column to increment
    # Returns True is increment is successful
    # Returns False if no record matches key or if target record is locked by 2PL.
    """
    def increment(self, key, column):
        r = self.select(key, self.table.key, [1] * self.table.num_columns)[0]
        if r is not False:
            updated_columns = [None] * self.table.num_columns
            updated_columns[column] = r[column] + 1
            u = self.update(key, *updated_columns)
            return u
        return False

