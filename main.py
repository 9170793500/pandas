
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




# # Doing for zip file
# import pandas as pd
# import zipfile
# import os

# excel_file = 'data_20231211.xlsx' 
# data = pd.read_excel(excel_file)

# output_file = 'data_20231211.xlsx' 
# data.to_excel(output_file, index=False)


# zip_file_name = 'data_20231211.zip' 
# with zipfile.ZipFile(zip_file_name, 'w') as zipf:
#     zipf.write(output_file)

# os.remove(output_file)








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
data = df.iloc[:, columns] #column select 

ceiled_pulse = df.iloc[:, 13].astype(float).apply(lambda x: m.ceil(x) // 15)

Equle_data = pd.concat([data, ceiled_pulse], axis=1)
Equle_data.columns = ['User', 'Date', 'Pulse'] #make in hedder 

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


# Reading data from the Excel file
excel_file = "sum_by_date.xlsx"
sdm = pd.read_excel(excel_file)
df = pd.DataFrame(sdm)

# Function to color with HTML table 
def table(df):
    colors = {
        'Date': '#FFFFE0',  # halka yellow
        'Total_Pulse': '#90EE90'  # light green
       
    }
    html_table = '<table style="border: 1px solid white; border-collapse: collapse;"><thead><tr>'
    
    # Add table  in header with  color
    for col in df.columns:
        html_table += f'<th style="padding: 5px; background-color: {colors.get(col, "white")}">{col}</th>'
    
    html_table += '</tr></thead><tbody>'
    
    # Add table rows with column
    for index, row in df.iterrows():
        html_table += '<tr>'
        for col in df.columns:
            html_table += f'<td style="padding: 5px; background-color: {colors.get(col, "white")}">{row[col]}</td>'
        html_table += '</tr>'
    
    html_table += '</tbody></table>'
    return html_table

data_html = table(df)

subject = "This is a check mail"
body_template = f"""
<html>
<head>
<style> 
  table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
  th, td {{ padding: 5px; }}
</style>
</head>

<body>
{data_html}
<br>
Regards,
Sundram Maurya
</body>
</html>
"""
# Email in with HTML body
msg = EmailMessage()
msg['From'] = 'interns@fonada.com'
# msg['To'] = 'mauryasundram1996@gmail.com'
msg['To'] = 'ravindra@fonada.com'
msg['Subject'] = subject
msg.add_alternative(body_template, subtype='html')

server = smtplib.SMTP('smtp.gmail.com', 587)
# Login  account email and password
server.starttls()
server.login('sundrammaurya1996@gmail.com', 'okua lodv qjve oszg')  # gmail with your password

with open("sum_by_date.xlsx", 'rb') as file:
    file_data = file.read()
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename='sum_by_date.xlsx')

server.send_message(msg)
server.quit()