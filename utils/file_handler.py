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
                    data.append('|'.join(row))
        return data
    except UnicodeDecodeError:
        print(f"File cannot be decoded using {file_encoder}")
        return []
    except FileNotFoundError:
        print (f"File not found")
        return []
    

# Task 1.2 - Parse and clean data

def parse_transactions(raw_lines):

    data= []
    for line in raw_lines:
        fields = [f.strip() for f in line.split('|')]
        t_id, dt, p_id, p_name, qty, price, c_id, region= fields
         # Skip rows with incorrect number of fields
        if len(fields) != 8:
            continue

        # Handles commas within product names by replacing commas with space....
        p_name_clean= p_name.replace(",", " ").strip()

        # Removes commas from numeric fields (eg. price = 45,000 or quantity = 10,000)
        qty_clean= qty.replace(",", "").strip()
        price_clean= price.replace(",", "").strip()

        try:
            qty= int(qty_clean)
            price= float(price_clean)
        except ValueError:
            continue
        
        data.append(
            {"TransactionID": t_id,
             "Date": dt,
             "ProductID": p_id,
             "ProductName": p_name_clean,
             "Quantity": qty,
             "UnitPrice": price,
             "CustomerID": c_id,
             "Region": region
             }
        )

    return data


# Task 1.3 Data Validation & Filtering

def validate_and_filter(transactions, region= None, min_amount= None, max_amount= None):
    # validates transactions and applies optional filters

    required_fields= [ 
        "TransactionID", "Date", "ProductID", "ProductName", 
        "Quantity", "UnitPrice", "CustomerID", "Region"
    ]
    
    total_input= len(transactions)
    invalid_count= 0
    valid_transactions= []
    # print all regions(from input, if present)...
    regions= sorted({
        t.get("Region", "").strip()
        for t in transactions
        if isinstance(t, dict) and t.get("Region")
    })
    print("Available regions:", regions if regions else "None Found")

    #---validate transactions-----
    for txn in transactions:
    # must be a dict
        if not isinstance(txn, dict):
            invalid_count += 1
            continue
    # all required fields must be non empty
        missing= [k for k in required_fields if k not in txn or txn.get(k) in (None, "")]
        if missing:
            invalid_count += 1
            continue
    # Fixing wrong ID formats
        if not str(txn["TransactionID"]).startswith("T"):
            invalid_count+= 1
            continue
        if not str(txn["ProductID"]).startswith("P"):
            invalid_count+= 1
            continue
        if not str(txn["CustomerID"]).startswith("C"):
            invalid_count+= 1
            continue
    # quantity and unit price must be positive
        try:
            qty= int(txn["Quantity"])
            price= float(txn["UnitPrice"])
        except (ValueError, TypeError):
            invalid_count+= 1
            continue
        if qty<= 0 or price <= 0:
            invalid_count+= 1
            continue
# stores normalised numeric values----
        txn["Quantity"]= qty
        txn["UnitPrice"]= price

        valid_transactions.append(txn)

# Amount range print--computed from valid transactions--
    if valid_transactions:
        amounts= [t["Quantity"]*t["UnitPrice"] for t in valid_transactions]
        print(f"Transaction amount range (valid only): min={min(amounts):.2f}, max= {max(amounts):.2f}")
    else:
        print(f"Transaction amoount range: No valid transactions to compute range.")

    # summary counters--
    filtered_by_region= 0
    filtered_by_amount= 0
    print(f"After validation:{len(valid_transactions)} records (Invalid:{invalid_count})")

    # Region filter--
    if region is not None:
        before= len(valid_transactions)
        valid_transactions= [t for t in valid_transactions if str(t.get("Region", "")).strip().lower()== str(region).strip().lower()]
        filtered_by_region= before- len(valid_transactions)
        print(f"After region filter({region}): {len(valid_transactions)} records")
    
    # Amount filters---
    def amount(t):
        return t["Quantity"]* t["UnitPrice"]
    
    if min_amount is not None:
        before= len(valid_transactions)
        valid_transactions= [t for t in valid_transactions if amount(t)>= float(min_amount)]
        filtered_by_amount+= before- len(valid_transactions)
        print(f"After min_amount filter ({min_amount}): {len(valid_transactions)} records")

    if max_amount is not None:
        before= len(valid_transactions)
        valid_transactions= [t for t in valid_transactions if amount(t)<= float(max_amount)]
        filtered_by_amount+= before- len(valid_transactions)
        print(f"After max_amount filter ({max_amount}): {len(valid_transactions)} records")

    filter_summary= {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    return filter_summary, valid_transactions

