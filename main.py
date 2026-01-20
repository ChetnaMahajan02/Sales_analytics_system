import os
from utils import file_handler, data_processor, api_handler, generate_sales_report
def main():
    # main execution function----
    try:
        print("="*40)
        print("SALES ANALYTICS SYSTEM")
        print("="*40)
        print()
    
    #-------------- (1/10) Read Sales data----------
        print("\n(1/10) Reading Sales data from file...")
        filename= "data/sales_data.txt"
        file_encoder= "utf-8"
        raw_lines= file_handler.read_sales_data(filename, file_encoder)
        print(f"Successfully read {len(raw_lines)} transactions.")
        if len(raw_lines) == 0:
            print("No data found.")
            return
        print()

    #-------------- (2/10) Parse and clean data----------
        print("\n(2/10) Parsing and cleaning sales data...")
        parsed_transactions= file_handler.parse_transactions(raw_lines)
        print(f"Parsed {len(parsed_transactions)} records.")
        if len(parsed_transactions) == 0:
            print("No valid transactions found")
            return
        print()

    #---------------(3/10) Filter options----------
        print("\n(3/10) Filter options available:")
        # available regions + max min amount range (from parsed data)
        regions= sorted({t.get("Region", "Unknown") for t in parsed_transactions if t.get("Region")})
        amounts= []
        for t in parsed_transactions:
            try:
                qty= int(t.get("Quantity", 0))
                price= float(t.get("UnitPrice", 0.0))
                amounts.append(qty * price)
            except Exception:
                pass
        print(f" Available Regions: {', '.join(regions)}")
        if amounts:
            min_amount_data= min(amounts)
            max_amount_data= max(amounts)
            print(f" Transaction Amount Range: ₹{min_amount_data:,.2f} to ₹{max_amount_data:,.2f}") 
        else:
            min_amount_data= None
            max_amount_data= None
            print("No transaction amounts available.")
            return
        print() 
        # Get user filter inputs    
        choice= input("\n Do you want to apply filters? (y/n): ").strip().lower()
        regions= None
        min_amount_data= None    
        max_amount_data= None
        if choice== 'y':
            region_input= input(" Enter Region to filter (leave blank for no region filter): ").strip()
            if region_input:
                regions= region_input
            min_amount_input= input(" Enter Minimum Amount to filter (leave blank for no min amount filter): ").strip()
            if min_amount_input:
                try:
                    min_amount_data= float(min_amount_input)
                except ValueError:
                    print(" Invalid minimum amount input.")
                    return
            max_amount_input= input(" Enter Maximum Amount to filter (leave blank for no max amount filter): ").strip()
            if max_amount_input:
                try:
                    max_amount_data= float(max_amount_input)
                except ValueError:
                    print(" Invalid maximum amount input.") 
                    return
        print()

    #-------------- (4/10) validate & filter ----------
        print("\n(4/10) Validating and filtering transactions...")  
        valid_transactions, filter_summary= file_handler.validate_and_filter(
            parsed_transactions,
            region= regions,
            min_amount= min_amount_data,
            max_amount= max_amount_data)
        print(f"|'Filter Summary:': {filter_summary}")
        if len(valid_transactions) == 0:
            print("No valid transactions after filtering. Exiting.")
            return
        print()        

    #--------------(5/10) Analysing Sales data----------------
     
        print("\n (5/10) Analyzing sales data...")
        total_revenue= data_processor.calculate_total_revenue(valid_transactions)
        print(f" Total Revenue Calculated: ₹{total_revenue:,.2f}")
        region_performance= data_processor.region_wise_sales(valid_transactions)
        print(f"region_performance: {region_performance}")
        top_products= data_processor.top_selling_products(valid_transactions, top_n=5)
        print(f" Top 5 Selling Products: {top_products}")
        customer_insights= data_processor.customer_analysis(valid_transactions)
        print(f" Customer Insights: {customer_insights}")
        daily_trends= data_processor.daily_sales_trend(valid_transactions)
        print(f" Daily Sales Trends: {daily_trends}")
        peak_revenue_days= data_processor.find_peak_sales_day(valid_transactions)
        print(f" Peak Revenue Days: {peak_revenue_days[:3]}")
        low_products= data_processor.low_performing_products(valid_transactions, threshold= 100.0)
        print(f" Low Performing Products: {low_products}")
        print()

                
    #---------------(6/10) Fetch API products-------
        print("\n(6/10) Fetching product details from API...")
        api_products= api_handler.fetch_all_products()
        print(f"Fetched {len(api_products)} products from API.")
        if len(api_products) == 0:
            print("No products fetched from API. Exiting.")
            return
        print()

    #---------------(7/10) Enrich Sales data--------
        product_mapping = api_handler.create_product_mapping(api_products)
        enriched_transactions = api_handler.enrich_sales_data(valid_transactions, product_mapping)
        print(f"Enriched {len(enriched_transactions)} transactions with product details.")
        enriched_success = sum(
        1 for t in enriched_transactions if t.get("api_match") is True)
        total_to_enrich = len(enriched_transactions)
        enriched_rate = (
        enriched_success / total_to_enrich * 100 if total_to_enrich > 0 else 0)

        print(
        f" - Successfully enriched: "
        f"{enriched_success}/{total_to_enrich} "
        f"transactions ({enriched_rate:.2f}%)")
        print()


    #--------------(8/10) Save enriched data to file--------
        print("\n(8/10) Saving enriched sales data to file...")
        enriched_file= "data/enriched_sales_data.txt"
        if os.path.exists(enriched_file):
            print(f" File already exists at {enriched_file}, skipping write.")
        else:           #...file already exists, skip writing
            print(f"(Enriched file {enriched_file} saved.)")
        print()

    #-------------(9/10) Generate Report--------
        print(f"\n (9/10) Generating sales report...")
        report_file= "output/sales_report.txt"   
        generate_sales_report.generate_sales_report(valid_transactions, enriched_transactions, output_file= report_file)
        print(f"Sales report generated at {report_file}.")
        print()

    #-------------(10/10) Completion Message--------
        print(f"\n (10/10) Process Complete!")
        print("="*40)
        print(f"Enriched data: {enriched_file}")
        print(f"Sales Report: {report_file}")
        print("="*40)
    except Exception as e:
        print(f"\n Something went wrong but the program did not crash")
        print(f" Error: {e}")

if __name__ == "__main__":
    main()

