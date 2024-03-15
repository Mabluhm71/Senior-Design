import os
import csv
#import importcsv

#C:\Users\mablu\OneDrive\Documents\Senior Design\PTO Testing

def parse_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Process each row as needed
            #print(row)
            return

def process_folder(folder_path):
    file_appendix = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.csv') and 'a' in file_name:
                file_path = os.path.join(root, file_name)
                print(f'Parsing CSV file: {file_path}')
                Analog_data = file_path
                file_appendix.append(Analog_data)
                parse_csv_file(file_path)
            elif file_name.endswith('.csv') and 'c' in file_name:
                file_path = os.path.join(root, file_name)
                print(f'Parsing CSV file: {file_path}')
                Encoder = file_path
                parse_csv_file(file_path)
                file_appendix.append(Encoder)
    return file_appendix            

folder_path = 'C:\\Users\\mablu\\OneDrive\\Documents\\Senior Design\\PTO Testing'

    

appendix = process_folder(folder_path)
