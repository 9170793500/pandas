
import pandas as pd
import zipfile
import io
import os

def data_header(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip:
        zip_files = zip.namelist()
        for file in zip_files:
            if file.endswith('.csv'):
                with zip.open(file) as csv_file:
                    df = pd.read_csv(io.TextIOWrapper(csv_file), low_memory=False)
                    print(len(df))
                    return df.columns.tolist()

def merge_csv(file_paths, new_file):
    header = data_header(file_paths[0])
    merged = pd.DataFrame(columns=header)

    for file_path in file_paths:
        with zipfile.ZipFile(file_path, 'r') as zip:
            zip_files = zip.namelist()
            for zip_file in zip_files:
                if zip_file.endswith('.csv'):
                    with zip.open(zip_file) as csv_file:
                        df = pd.read_csv(io.TextIOWrapper(csv_file), low_memory=False)
                        if merged.empty:
                            merged = df.copy()
                            print("Success")
                        else:
                            merged = pd.concat([merged, df], ignore_index=True)
                
    csv_buffer = io.StringIO()
    merged.to_csv(csv_buffer, index=False)
    print("Total merge file row count:", len(merged))
    csv_buffer.seek(0)

    with zipfile.ZipFile(new_file, 'w', zipfile.ZIP_DEFLATED) as zip_output:
        zip_output.writestr('merged_data.csv', csv_buffer.getvalue())

# globle path select folder
def merge_files_folder(folder_path, new_zip):
    folder = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file)) and file.endswith('.zip')]
    
    new_folder = os.path.join(folder_path, 'Merged_Files')


    zip_file_path = os.path.join(new_folder, new_zip)

    merge_csv(folder, zip_file_path)

folder_path = '/home/niromoney' 

# New file name for merged data
new_file = 'new_file_merge.zip'

merge_files_folder(folder_path, new_file)












# import zipfile
# import pandas as pd
# import io



# # List of ZIP files
# data =  ['1703292302138_FTP_CdrShortReportLead_USER_116_FB_22_12_HPMP_ABC_M2_xmas-2-5k_2524_34837_MLT_M3_22-12-2023-TO-22-12-2023.csv.zip', 
#         '1703292302608_FTP_CdrShortReportLead_USER_116_FB_22_12_HPMP_ABC_M2_cg_1944_34838_MLT_M3_22-12-2023-TO-22-12-2023.csv.zip',
#         '1703292302772_FTP_CdrShortReportLead_USER_116_FB_26_12_LP_ABCD_M1_cg-testt_1981_34885_MLT_M3_22-12-2023-TO-22-12-2023.csv.zip',
#         '1703292302858_FTP_CdrShortReportLead_USER_116_FB_26_12_LP_ABCD_M1_final-emi-5k-testt_2544_34887_MLT_M3_22-12-2023-TO-22-12-2023.csv.zip',
#         '1703292302939_FTP_CdrShortReportLead_USER_116_Niro_26_12_HPMP_ABC_M2_cg-test_1980_34891_MLT_M3_22-12-2023-TO-22-12-2023.csv.zip',
#         '1703292303113_FTP_CdrShortReportLead_USER_116_FB_26_12_HPMP_ABC_M2_cg-testt_1981_34893_MLT_M3_22-12-2023-TO-22-12-2023.csv.zip',
#         '1703292303196_FTP_CdrShortReportLead_USER_116_FB_26_12_HPMP_ABC_M2_final-emi-5k-testt_2544_34894_MLT_M3_22-12-2023-TO-22-12-2023.csv.zip'
#         ]
# # Extract header from the first CSV file inside the ZIP
# def data_header(file_path):
#     with zipfile.ZipFile(file_path, 'r') as zip:
#         zip_files = zip.namelist()
#         for file in zip_files:
#             if file.endswith('.csv'):
#                 with zip.open(file) as csv_file:
#                     df = pd.read_csv(io.TextIOWrapper(csv_file),low_memory=False)
#                     print(len(df))
#                     return df.columns.tolist()

# # Merge CSV files and create new ZIP with merged data
# def merge_csv(files, new_file):
#     header = data_header(files[0])
#     merged = pd.DataFrame(columns=header)

#     for file in files:
#         with zipfile.ZipFile(file, 'r') as zip:
#             zip_files = zip.namelist()
#             for zip_file in zip_files:
#                 if zip_file.endswith('.csv'):
#                     with zip.open(zip_file) as csv_file:
#                         df = pd.read_csv(io.TextIOWrapper(csv_file), low_memory=False)
#                         if merged.empty:
#                             merged = df.copy()
#                             print("Success")
#                         else:
#                             merged = pd.concat([merged, df], ignore_index=True)
                
#     # Save merged data csv 
#     csv_buffer = io.StringIO()
#     merged.to_csv(csv_buffer, index=False)
#     print("Total merge file row count:", len(merged))  # total file row count data
#     csv_buffer.seek(0)

#     #  new ZIP file merged CSV data
#     with zipfile.ZipFile(new_file, 'w', zipfile.ZIP_DEFLATED) as zip_output:
#         zip_output.writestr('merged_data.csv', csv_buffer.getvalue())
        
# # merge new file name
# new_zip_file = 'new_file_merge.zip'

# # function call to run
# merge_csv(data, new_zip_file)






# #  Doing for zip file unzip   to excel

# import zipfile
# #  read to zip file 
# with zipfile.ZipFile('merged.zip' , 'r') as zip_ref:
   
#     file_list = zip_ref.namelist()
#     for file in file_list:
#         print(file)

#     zip_file = 'New_sdm' 
#     zip_ref.extractall(zip_file)
#     print(f"All files extracted to {zip_file}")











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




# from openpyxl import load_workbook
# from openpyxl.styles import PatternFill
# import pandas as pd
# import math as m
# import smtplib
# from email.message import EmailMessage
# from sqlalchemy import create_engine

# df = pd.read_csv('master.csv', header=None)
# columns = [3, 9]
# data = df.iloc[:, columns] #column select 

# ceiled_pulse = df.iloc[:, 13].astype(float).apply(lambda x: m.ceil(x) // 15)

# Equle_data = pd.concat([data, ceiled_pulse], axis=1)
# Equle_data.columns = ['User', 'Date', 'Pulse'] #make in hedder 

# df = pd.DataFrame(Equle_data)

# df['Date'] = pd.to_datetime(df['Date'])
# df['Date'] = df['Date'].dt.date

# Equle_data.insert(0, 'id', range(1, len(Equle_data) + 1))
# grouped = df.groupby(['User', 'Date'])['Pulse'].sum().reset_index() 
# grouped.columns = ['User','Date', 'Total_Pulse']


# print(grouped.head())

# grouped.to_excel("sum_by_date.xlsx", sheet_name="Sum_By_Date", index=False)

# # database connection
# database_uri = 'mysql+pymysql://root:@localhost/s'
# engine = create_engine(database_uri)
# query = "SELECT * FROM excel"
# try:
#   grouped.to_sql(name='excel', con=engine, if_exists='replace', index=False)
#   print("succes")  
# except:
#     print("not") 


# # Reading data from the Excel file
# excel_file = "sum_by_date.xlsx"
# sdm = pd.read_excel(excel_file)
# df = pd.DataFrame(sdm)

# # Function to color with HTML table 
# def table(df):
#     colors = {
#         'Date': '#FFFFE0',  # light yellow
#         'Total_Pulse': '#90EE90'  # light green
       
#     }
#     html_table = '<table style="border: 1px solid white; border-collapse: collapse;"><thead><tr>'
    
#     # Add table  in header with  color
#     for col in df.columns:
#         html_table += f'<th style="padding: 5px; background-color: {colors.get(col, "white")}">{col}</th>'
    
#     html_table += '</tr></thead><tbody>'
    
#     # Add table rows with column
#     for index, row in df.iterrows():
#         html_table += '<tr>'
#         for col in df.columns:
#             html_table += f'<td style="padding: 5px; background-color: {colors.get(col, "white")}">{row[col]}</td>'
#         html_table += '</tr>'
    
#     html_table += '</tbody></table>'
#     return html_table


# data_html = table(df)

# subject = "This is a check mail"
# body_template = f"""
# <html>
# <head>
# <style> 
#   table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
#   th, td {{ padding: 5px; }}
# </style>
# </head>

# <body>
# {data_html}
# <br>
# Regards,
# Sundram Maurya
# </body>
# </html>
# """
# # Email in with HTML body
# msg = EmailMessage()
# msg['From'] = 'interns@fonada.com'
# # msg['To'] = 'mauryasundram1996@gmail.com'
# msg['To'] = 'ravindra@fonada.com'
# msg['Subject'] = subject
# msg.add_alternative(body_template, subtype='html')

# server = smtplib.SMTP('smtp.gmail.com', 587)
# # Login  account email and password
# server.starttls()
# server.login('sundrammaurya1996@gmail.com', 'okua lodv qjve oszg')  # gmail with your password

# with open("sum_by_date.xlsx", 'rb') as file:
#     file_data = file.read()
#     msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename='sum_by_date.xlsx')

# server.send_message(msg)
# server.quit()






