
# coding: utf-8

# In[1]:

import pyspark
sc = pyspark.SparkContext('local[*]')

# do something to prove it works
rdd = sc.parallelize(range(1000))
rdd.takeSample(False, 5)


# In[18]:

import random
import time
import string
from datetime import datetime
from time import mktime

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)
    dt = datetime.fromtimestamp(mktime(time.localtime(ptime)))
    return  dt


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %H:%M:%S', prop)

def rdString(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


# In[99]:

from pyspark.sql import Row
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
ids = [rdString(6) for _ in xrange(5)]
raw_data = []
raw_data_2 = []
for id in ids:
    for _ in xrange(random.randint(1,3)):
        tmp = Row(id_1=id,date_1=randomDate("1/1/2008 10:30:10", "1/1/2010 14:50:20", random.random()))
        raw_data.append(tmp)

    for _ in xrange(random.randint(0,5)):
        tmp = Row(id_2=id,date_2=randomDate("1/1/2008 10:30:10", "1/1/2012 14:50:20", random.random()))
        raw_data_2.append(tmp)


# In[100]:

df1 = sqlContext.createDataFrame(raw_data)
df2 = sqlContext.createDataFrame(raw_data_2)
print '---df1---'
df1.show()
print '---df2---'
df2.show()


# In[101]:

import json
def get_rdd_date(df1,keys):
    rdd1 = df1.rdd.map(lambda x : (x['id_1'],[x['date_1']]))                .reduceByKey(lambda x,y : x+y).map(lambda x : (x[0],sorted(list(set(x[1])), reverse=True)) )

rdd1.take(5)


# In[123]:

from pyspark.sql import DataFrame

def unionAll(*dfs):
    return reduce(DataFrame.unionAll, dfs)
all_df = []
counter = 0
for d in rdd1.collect():
    filters_1 = df1.filter((df1['id_1']==d[0]) & (df1['date_1'] == d[1][0]))
    filters_2 = df2.filter((df2['id_2']==d[0]))# & (df2['date_2'] <= d[1][0]))
    joined_1 = filters_1.join(filters_2,filters_1['id_1']==filters_2['id_2'],"inner")
    print "%d total data joined_1 " % (joined_1.count(),)
    counter += joined_1.count()
    all_df.append(joined_1)
    print "%d dates"% (len(d[1]),)
    if len(d[1]) >1:
        for i in xrange(1,len(d[1])):
            print "date number %d" % (i,)
            filters_1 = df1.filter((df1['id_1']==d[0]) & (d[1][i] == df1['date_1'] )) 
            filters_2 = df2.filter((df2['id_2']==d[0]) & (df2['date_2'] <= d[1][i-1]) )
            joined = filters_1.join(filters_2,filters_1['id_1']==filters_2['id_2'],"inner")
            print "%d total data joined" % (joined.count(),)
            counter += joined.count()
            all_df.append(joined)
            
df = unionAll(*all_df)
print counter
df.show()
#join = df1.join(df2, df1['id_1'] == df2['id_2'], "inner").filter(df2['date_2'] < df1['date_1'])
#join.show()
#filters.show()


# In[ ]:



