
# #  Doing for zip file unzip   to excel

# import zipfile


# #  read to zip file 
# with zipfile.ZipFile('merged_daa.zip' , 'r') as zip_ref:
   
#     file_list = zip_ref.namelist()
#     for file in file_list:
#         print(file)

#     zip_file = 'New_sdm' 
#     zip_ref.extractall(zip_file)
#     print(f"All files extracted to {zip_file}")




# Doing for zip file
import pandas as pd
import zipfile
import os

excel_file = 'data_20231211.xlsx' 
data = pd.read_excel(excel_file)

output_file = 'data_20231211.xlsx' 
data.to_excel(output_file, index=False)


zip_file_name = 'data_20231211.zip' 
with zipfile.ZipFile(zip_file_name, 'w') as zipf:
    zipf.write(output_file)

os.remove(output_file)








# # 4 csv file merge and single header 

# import pandas as pd

# files = ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv']  


# sdm = []

# for file in files:
#     df = pd.read_csv(file, header=0)
    
#     sdm.append(df)

# merged_df = pd.concat(sdm)

# merged_df.to_excel("merged_daa.xlsx", sheet_name="Merged_Data", index=False)

# print(merged_df.info())





# import pandas as pd
# from datetime import datetime

# data = pd.read_excel('New_sdm/output_merged_daa.xlsx')

# current_date = datetime.now().strftime("%Y%m%d")

# file_name = f"data_{current_date}.xlsx" 

# s=data.to_excel(file_name, index=False)  
# print(s)




from openpyxl import load_workbook
from openpyxl.styles import PatternFill
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

# database connection
database_uri = 'mysql+pymysql://root:@localhost/s'
engine = create_engine(database_uri)
query = "SELECT * FROM excel"
try:
  grouped.to_sql(name='excel', con=engine, if_exists='replace', index=False)
  print("succes")  
except:
    print("not") 



excel_file = "sum_by_date.xlsx"
df = pd.read_excel(excel_file)

columns_to_color = {'Date': 'blue', 'Total_Pulse': 'green'}  # Specify columns and their respective colors
data_text = df.to_html(index=False, border=1, escape=True)

for column, color in columns_to_color.items():
    # Apply color to the header cells of the respective columns
  
    data_text = data_text.replace(f'<th>{column}</th>', f'<th style="background-color: {color}; color: white;">{column}</th>')

    # Apply color to all cells of the respective column using a class or unique identifier
    data_text = data_text.replace(f'<td>{column}</td>', f'<td class="{column}_class" style="background-color: {color}; color: white;">{column}</td>')


# Email body template
subject = "This is a check mail"
body_template = f'''
Hello,
Sir, work is complete.

This is the data you requested:<br><br>

{data_text}<br><br>

Regards,
Sundram Maurya
'''

# Email composition with HTML body
msg = EmailMessage()
msg['From'] = 'sundrammaurya1996@gmail.com'
msg['To'] = 'mauryasundram1996@gmail.com'
msg['Subject'] = subject
msg.add_alternative(body_template, subtype='html')

server = smtplib.SMTP('smtp.gmail.com', 587)
# Login  account email and password
server.starttls()
server.login('sundrammaurya1996@gmail.com', 'okua lodv qjve oszg')  # Update with your password

with open("sum_by_date.xlsx", 'rb') as file:
    file_data = file.read()
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename='sum_by_date.xlsx')

server.send_message(msg)
server.quit()