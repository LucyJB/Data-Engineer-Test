import pandas as pd
import sqlite3
import numpy as np

#1. Setup the database in local sql install
conn = sqlite3.connect('test_database')
c = conn.cursor()
columns = ('Index', 'productName', 'Creator', 'creatorID', 'profit', 'revenue', 'cost', 'location', 'category', 'samplePerc')


c.execute('CREATE TABLE IF NOT EXISTS products(columns)')
conn.commit()

# creating dataframe from csv
df = pd.read_csv("sampledata.csv", encoding= 'unicode_escape')

#remove any duplicate entries
df_duplicates_removed = df.drop_duplicates()
print(df_duplicates_removed)

#rename the column name 'Index' to id to prevent issues further on
df.rename(columns = {'Index':'Id'}, inplace = True)

# Question 2. computing number of rows
rows = len(df.axes[0])
print (rows)

df.to_sql('products', conn, if_exists='replace', index = False)

#Question 3a.Showing sum of reveue by Creator
for revenue_sum in c.execute('''
SELECT Creator , sum(revenue)
FROM products
group by Creator
order by Creator
          '''):
          print (revenue_sum)


#Question 3b.Showing count of products by Creator
for product_count in c.execute('''
SELECT Creator , count(productName)
FROM products
group by Creator
order by Creator
          '''):
    print (product_count)


#Question 3c.Showing sum of profits by Creator
for profit_sum in c.execute('''
SELECT Creator , sum(profit)
FROM products
group by Creator
order by Creator
          '''):
    print (profit_sum)


#close connnection
c.close
