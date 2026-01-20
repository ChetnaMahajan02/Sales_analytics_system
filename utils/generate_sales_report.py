import os
from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file= "output/sales_report.txt"):
    #-------------------1) Header -------------------
    now= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records= len(transactions)

    #------------- 2) Overall Summary --------------
    total_revenue= 0.0
    total_transactions= 0
    for t in transactions:
        try:
            qty= int(t.get("Quantity", 0))
            price= float(t.get("UnitPrice", 0.0))
            total_revenue += qty * price
            total_transactions += 1
        except Exception:
            continue
    avg_order_value= (total_revenue / total_transactions) if total_transactions > 0 else 0.0
    min_date, max_date= None, None
    for t in transactions:
        dt_str= str(t.get("Date", "")).strip()
        try:
            dt= datetime.strptime(dt_str, "%Y-%m-%d")
            if min_date is None or dt < min_date:
                min_date= dt
            if max_date is None or dt > max_date:
                max_date= dt
        except Exception:
            continue
        #------------- 3) Region-wise Performance --------------
    region_sales= {}
    grand_total= 0.0    
    for t in transactions:
        try:
            region= str(t.get("Region", "Unknown")).strip()
            qty= int(t.get("Quantity", 0))
            price= float(t.get("UnitPrice", 0.0))
            amount= qty * price
            grand_total += amount
        except Exception:
            continue
        if region not in region_sales:
            region_sales[region]= {
                "total_sales": 0.0,
                "transaction_count": 0
            }
        region_sales[region]["transaction_count"] += 1
        region_sales[region]["total_sales"] += amount
    region_rows= []
    for region, data in sorted(region_sales.items(), key= lambda item: item[1]["total_sales"], reverse= True):
        pct= (data["total_sales"] / grand_total) * 100 if grand_total > 0 else 0.0
        region_rows.append((
            region,
            data['total_sales'],
            grand_total,
            pct,
            data["transaction_count"]
        ))
    
        
    #------------- 4) Top 5 Products --------------
    product_sales= {}
    for t in transactions:
        try:
            p_name= str(t.get("ProductName", "Unknown")).strip()
            qty= int(t.get("Quantity", 0))
            price= float(t.get("UnitPrice", 0.0))
            revenue= qty * price
        except Exception:
            continue
        if p_name not in product_sales:
            product_sales[p_name]= {
            "total_sales": 0.0,
            "total_quantity": 0
            }
        product_sales[p_name]["total_sales"] += revenue
        product_sales[p_name]["total_quantity"] += qty
    top_products= sorted(
        product_sales.items(),
        key= lambda item: item[1]["total_sales"],
        reverse= True
    )[:5]

#------------- 5) Top 5 Customers --------------
    customer_data= {}
    for t in transactions:
        try:
            c_id= str(t.get("CustomerID", "Unknown")).strip()
            p_name= str(t.get("ProductName", "Unknown")).strip()
            qty= int(t.get("Quantity", 0))
            price= float(t.get("UnitPrice", 0.0))
            amount= qty * price
        except Exception:
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
    top_customers= sorted(
        customer_data.items(),
        key= lambda item: item[1]["total_spent"],
        reverse= True
        )[:5]

    #------------- 6) Daily Sales Trend --------------
   
    daily_data = {}

    for t in transactions:
        try:
            date = str(t.get("Date", "")).strip()
            customer = str(t.get("CustomerID", "Unknown")).strip()
            qty = int(t.get("Quantity", 0))
            price = float(t.get("UnitPrice", 0.0))
            amount = qty * price
        except Exception:
            continue

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "txn_count": 0,
                "unique_customers": set()
            }

        daily_data[date]["revenue"] += amount
        daily_data[date]["txn_count"] += 1
        daily_data[date]["unique_customers"].add(customer)

    daily_rows = [
        (
        d,
        v["revenue"],
        v["txn_count"],
        len(v["unique_customers"])
        )
        for d, v in sorted(daily_data.items())
    ] 
    #------------- 7) Product Performance Analysis --------------

    # Best selling day---
    if daily_rows:
        best_day= max(daily_rows, key=lambda x:x [1])
        best_selling= (best_day[0], best_day[1], best_day[2])
    else:
        best_selling= (None, 0.0, 0)
    

    print(f"Generating sales report at {now} with {total_records} records.")
    with open(output_file, "w", encoding= "utf-8") as f:
        f.write(" "*25 + "SALES REPORT\n")
        f.write(f"Generated on: {now}\n")
        f.write(f"Total Transactions Analyzed: {total_records}\n")
        f.write("="*50 + "\n\n")

        f.write("\nOVERALL SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"total_revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"total_transactions: {total_transactions}\n")
        f.write(f"average_order_value: ₹{avg_order_value:,.2f}\n")
        f.write(f"date_range: {min_date.strftime('%Y-%m-%d') if min_date else 'N/A'} to {max_date.strftime('%Y-%m-%d') if max_date else 'N/A'}\n")
        
        f.write("\nREGION-WISE PERFORMANCE\n")
        f.write("-"*50 + "\n")
        f.write("Region         Total Sales        Amount      Percentage of total     Transaction Count\n")
        for region, total_sales, amount, percentage, transaction_count in region_rows:
            f.write(
                f"{region:<15}  "
                f"₹{total_sales:,.2f}  "
                f"₹{amount:,.2f}  "
                f"{percentage:.2f}%  "
                f"{transaction_count}\n"
            )
            
        f.write("\nTOP 5 PRODUCTS\n")
        f.write("-"*50 + "\n")
        f.write("Product Name         Quantity Sold     Revenue\n")
        for product, data in top_products:
            f.write(
                f"{product:<20}" 
                f"{data['total_quantity']}"
                f"₹{data['total_sales']:,.2f}\n"
            )
            
        f.write("\nTOP 5 CUSTOMERS\n")
        f.write("-"*50 + "\n")
        f.write("Customer ID         Total Spent     Order_count\n")
        for customer_id, data in top_customers:
            f.write(f"{customer_id:<20}"
                    f"₹{data['total_spent']:,.2f}"
                    f"{data['purchase_count']}\n")
            
        f.write("\nDAILY SALES TREND\n")
        f.write("-"*50 + "\n")
        f.write("Date          Revenue      Transactions        unique_customers\n")
        for date, revenue, transaction_count, unique_customers in daily_rows: 
            f.write(f"{date:<15}"
                    f"₹{revenue:,.2f}"
                    f"{transaction_count}"
                    f"{unique_customers}\n")
            
        f.write("\nPRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-"*50 + "\n")
        f.write(f"Best Selling Day: {best_selling}")

        f.write("\n API ENRICHED DATA SUMMARY\n")
        f.write("-"*50 + "\n")
        total_enriched= len([t for t in enriched_transactions if t.get("API_match") is True])
        f.write(f"Total Products Enriched: {total_enriched} out of {total_records}\n")
        success_rate= (total_enriched / total_records * 100) if total_records > 0 else 0.0
        f.write(f"Enrichment Success Rate: {success_rate:.2f}%\n")
        not_enriched= total_records - total_enriched
        f.write(f"Products Not Enriched: {not_enriched}\n")
    print(f"Sales report generated at {output_file}")