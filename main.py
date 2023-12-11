
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
