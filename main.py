
import smtplib
import numpy as np
import pandas as pd 
from openpyxl import Workbook
wb = Workbook()

# grab the active worksheet
ws = wb.active


# s = pd.Series(Data)
# dataframe=pd.DataFrame({'num':[1, 3, 4, 5, 6, 2, 9],
#                        'sdm':['a','s','d','f','g','h','k']})
# s=dataframe.count()

# print(s)

# sd= pd.read_csv('studentData.csv')

# print(sd)
# print(sd.head(5))
# print(sd.tail(5))
# print(sd.info())


# sd= pd.read_csv('studentData.csv')
# sdm = sd.dropna()
# print(sdm.to_string)


# sd= pd.read_csv('studentData.csv')
# sd.dropna(inplace=True)
# print(sd.to_string())


# Automatice nan data fill karana mean(),mode()with indexing, median() type se 

sd= pd.read_csv('studentData.csv')
sd.fillna(130 ,inplace=True)
# print(sd.to_string())

sharad = pd.read_csv('studentData.csv')
x = sharad["height"].mode()[0]
sharad["height"].fillna(x, inplace=True)
# print(sharad.to_string())

sharad = pd.read_csv('studentData.csv')
x = sharad["height"].mean()
sharad["height"].fillna(x, inplace=True)
# print(sharad.to_string())

sharad = pd.read_csv('studentData.csv')
x = sharad["height"].median()
sharad["height"].fillna(x, inplace=True)
# print(sharad.to_string())





df = pd.read_csv('studentData.csv')
sdm= df.groupby(['height']).sum()
# print(sdm)


Data = {'Gender':[172,169,169,173,17,17,178],'Height':[172,169,169,173,17,17,178]}
df = pd.DataFrame(Data)
sdm= df.groupby(['Height'])
a = sdm.sum()
# print(a)


# data row count file in all
dataframe = pd.read_csv('studentData.csv')
s=dataframe.count()


# print(f'The DataFrame has {s} rows.')

# print("Total Null values count: ",
#       dataframe.isnull().sum().sum())


df1 = pd.read_csv('studentData.csv')
sdm =df1['number'].sum()

# print(sdm)





import pandas as pd
import math as m
import smtplib
from email.message import EmailMessage
from sqlalchemy import create_engine



df = pd.read_csv('master.csv', header=None)
columns = [3, 9]
data = df.iloc[:, columns]

ceiled_pulse = df.iloc[:, 13].astype(float).apply(lambda x: m.ceil(x) // 15)


Equle_data = pd.concat([data, ceiled_pulse], axis=1)
Equle_data.columns = ['User', 'Date', 'Pulse']

df = pd.DataFrame(Equle_data)

df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.date

Equle_data.insert(0, 'id', range(1, len(Equle_data) + 1))
grouped = df.groupby(['User', 'Date'])['Pulse'].sum().reset_index()
grouped.columns = ['User','Date', 'Total_Pulse']



print(grouped.head())

grouped.to_excel("sum_by_date.xlsx", sheet_name="Sum_By_Date", index=False)

#database connection
database_uri = 'mysql+pymysql://root:@localhost/s'
engine = create_engine(database_uri)
query = "SELECT * FROM excel"
try:
  grouped.to_sql(name='excel', con=engine, if_exists='replace', index=False)
  print("succes")  
except:
    print("not") 

engine.dispose() 


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('sundrammaurya1996@gmail.com', 'okua lodv qjve oszg')

subject = "This is a check mail"
body_template = '''Hello,\n  sir work is complete \n\nThis is the data you requested:\n
\n{data_text}\n\n
Regards,\n
Sundram Maurya'''

data_text = grouped.to_html(index=False, border=1)
data_text = data_text.replace('<th>', '<th style="background-color: blue; color: white;">')
data_text = data_text.replace('<tr>', '<tr style="background-color: aqua; color: balck;">')

email_body = body_template.format(data_text=data_text)

msg = EmailMessage()
msg['From'] = 'sundrammaurya1996@gmail.com'
msg['To'] = 'mauryasundram1996@gmail.com'
# msg['To'] = 'ravindra@fonada.com'
msg['Subject'] = subject
msg.add_alternative(email_body, subtype='html')

with open("sum_by_date.xlsx", 'rb') as file:
    file_data = file.read()
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename='sum_by_date.xlsx')
  

server.send_message(msg)
server.quit()





