## Task 1.1  Read Sales data with Encoding handling

import csv

def read_sales_data(filename, file_encoder):
    try:
        data= []
        with open(filename, mode= "r", encoding= file_encoder, newline= "\n") as file:
            file_data= csv.reader(file, delimiter="|")
            next(file_data)   # skips header
            for row in file_data:
                if row and any(field.strip() for field in row):  # removes empty lines
                    print (row)
        return data
    except FileNotFoundError:
        print ("File not found")
    return []
read_sales_data("data/sales_data.txt", "utf-8")