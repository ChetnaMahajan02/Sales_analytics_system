# DATA PRE-PROCESSOR-----
# TASK 2.1- SALES SUMMARY CALCULATOR---

# a) Calculate Total Revenue-
def calculate_total_revenue(transactions):
    total_revenue= 0.0
    for txn in transactions:
        try:
            qty= int(txn.get("Quantity", 0))
            price= float(txn.get("UnitPrice", 0.0))
            total_revenue += qty * price
        except (ValueError, TypeError, KeyError):
            continue
    return round(total_revenue, 2)

# b) Region wise sales analysis-
def region_wise_sales(transactions):
    region_sales= {}
    grand_total= 0.0    
    # aggregate sales by region and count by region
    for txn in transactions:
        try:
            region= str(txn.get("Region", "Unknown")).strip()
            qty= int(txn.get("Quantity", 0))
            price= float(txn.get("UnitPrice", 0.0))
            amount= qty * price
            grand_total += amount
        except (ValueError, TypeError, KeyError):
            continue
        if region not in region_sales:
            region_sales[region]= {
                "total_sales": 0.0,
                "transaction_count": 0
            }
        region_sales[region]["transaction_count"] += 1
        region_sales[region]["total_sales"] += amount
        
    # calculate percentage contribution
    for region in region_sales:
        if grand_total > 0:
            pct= (region_sales[region]["total_sales"] / grand_total) * 100   
        else:
            pct= 0.0
        region_sales[region]["percentage_contribution"]= round(pct, 2)
        region_sales[region]["total_sales"]= round(region_sales[region]["total_sales"], 2)
   
   # sort regions by total sales in descending order
    sorted_region_sales= dict(
        sorted(
            region_sales.items(),
            key= lambda item: item[1]["total_sales"],
            reverse= True
        )
    )
    return sorted_region_sales

# c) Top Selling Products---
def top_selling_products(transactions, top_n):
    product_sales= {}
    # aggregate sales by product
    for txn in transactions:
        try:
            p_name= str(txn.get("ProductName", "Unknown")).strip()
            qty= int(txn.get("Quantity", 0))
            price= float(txn.get("UnitPrice", 0.0))
            revenue= qty * price
        except (ValueError, TypeError, KeyError):
            continue
        if p_name not in product_sales:
            product_sales[p_name]= {
                "ProductName": p_name,
                "total_sales": 0.0,
                "total_quantity": 0
            }
        product_sales[p_name]["total_sales"] += revenue
        product_sales[p_name]["total_quantity"] += qty

    # sort products by total sales in descending order
    sorted_products= sorted(
        product_sales.items(),
        key= lambda item: item[1]["total_sales"],
        reverse= True

    )
    # return top N products in tuple format
    top_n= [
        (prod[1]["ProductName"], prod[1]["total_quantity"], round(prod[1]["total_sales"], 2))
        for prod in sorted_products[:top_n]
    ]
    return top_n

# d) Customer Purchase Analysis--- 

def customer_analysis(transactions):
    customer_data= {}
    # aggregate data by customer
    for txn in transactions:
        try:
            c_id= str(txn.get("CustomerID", "Unknown")).strip()
            p_name= str(txn.get("ProductName", "Unknown")).strip()
            qty= int(txn.get("Quantity", 0))
            price= float(txn.get("UnitPrice", 0.0))
            amount= qty * price
        except (ValueError, TypeError, KeyError):
            continue
        if c_id not in customer_data:
            customer_data[c_id]= {
                "total_spent": 0.0,
                "purchase_count": 0,
                "unique_products": set()
            }
        customer_data[c_id]["total_spent"] += amount
        customer_data[c_id]["purchase_count"] += 1
        customer_data[c_id]["unique_products"].add(p_name)

    # prepare final data with average order value and convert unique products set to count
    final_customer_data= []
    for c_id, data in customer_data.items():
        avg_order_value= data["total_spent"] / data["purchase_count"] if data["purchase_count"] > 0 else 0.0
        final_customer_data.append({
            "CustomerID": c_id,
            "TotalSpent": round(data["total_spent"], 2),
            "PurchaseCount": data["purchase_count"],
            "AverageOrderValue": round(avg_order_value, 2),
            "UniqueProductsBought": len(data["unique_products"])
        })

    # sort customers by total spent in descending order
    sorted_customers= sorted(
        final_customer_data,
        key= lambda item: item["TotalSpent"],
        reverse= True
    )
    return sorted_customers

# TASK 2.2: Date based Analysis

# a) Daily Sales trend group by date, calculate daily revenue, count daily transactions, count unique customers per day and sort chronologically.

def daily_sales_trend(transactions):
    daily_data= {}
    # aggregate data by date
    for txn in transactions:
        try:
            dt= str(txn.get("Date", "Unknown")).strip()
            c_id= str(txn.get("CustomerID", "Unknown")).strip()
            qty= int(txn.get("Quantity", 0))
            price= float(txn.get("UnitPrice", 0.0))
            amount= qty * price
        except (ValueError, TypeError, KeyError):
            continue
        if dt not in daily_data:
            daily_data[dt]= {
                "total_revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }
        daily_data[dt]["total_revenue"] += amount
        daily_data[dt]["transaction_count"] += 1
        if c_id:
            daily_data[dt]["unique_customers"].add(c_id)

    # prepare final data with unique customer count
    final_daily_data= []
    for dt, data in daily_data.items():
        final_daily_data.append({
            "Date": dt,
            "TotalRevenue": round(data["total_revenue"], 2),
            "TransactionCount": data["transaction_count"],
            "UniqueCustomers": len(data["unique_customers"])
        })

    # sort daily data chronologically by date
    sorted_daily_data= sorted(
        final_daily_data,
        key= lambda item: item["Date"]
    )
    return sorted_daily_data

# b) Find peak sales day identifying date with highest revenue and transaction count

def find_peak_sales_day(transactions):
    daily= {}
    for txn in transactions:
        try:
            dt= str(txn.get("Date", "Unknown")).strip()
            qty= int(txn.get("Quantity", 0))
            price= float(txn.get("UnitPrice", 0.0))
            amount= qty * price
        except (ValueError, TypeError, KeyError):
            continue
        if dt not in daily:
            daily[dt]= {
                "total_revenue": 0.0,
                "transaction_count": 0
            }
        daily[dt]["total_revenue"] += amount
        daily[dt]["transaction_count"] += 1
    if not daily:
        return None, 0, 0.0
    # find peak revenue day
    peak_revenue_day= max(
        daily.items(),
        key= lambda item: item[1]["total_revenue"]
    )
    return peak_revenue_day[0], peak_revenue_day[1]["transaction_count"], peak_revenue_day[1]["total_revenue"]

# TASK 2.3: Product Performance
# a) Low performing products - identify products with sales below a certain threshold

def low_performing_products(transactions, threshold= 10):
    product_sales= {}
    # aggregate sales by product and revenue
    for txn in transactions:
        try:
            p_name= str(txn.get("ProductName", "Unknown")).strip()
            qty= int(txn.get("Quantity", 0))
            price= float(txn.get("UnitPrice", 0.0))
            revenue= qty * price
        except (ValueError, TypeError, KeyError):
            continue

        if p_name not in product_sales:
            product_sales[p_name]= {"total_quantity": 0.0, "total_revenue": 0.0}
        product_sales[p_name]["total_quantity"] += qty
        product_sales[p_name]["total_revenue"] += revenue

    # identify low performing products
    low_products= [
        (p_name, data["total_quantity"], round(data["total_revenue"], 2))
        for p_name, data in product_sales.items()
        if data["total_quantity"] < threshold
    ]
    # sort by total quantity ascending
    low_products.sort(key= lambda item: item[1])
    return low_products