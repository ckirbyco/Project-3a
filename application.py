import requests
import matplotlib.pyplot as plt

#Stock data function to query API
def get_stock_data(symbol, function, start_date, end_date, api_key, interval=None):
    if function.startswith('TIME_SERIES_INTRADAY'):
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={api_key}&outputsize=full"
    else:
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}&outputsize=full"
    
    response = requests.get(url)
    data = response.json()
    
    if function.startswith('TIME_SERIES_INTRADAY'):
        time_series_key = next((key for key in data.keys() if "Time Series" in key), None)
        if not time_series_key:
            print("Error: Intraday data not found in API response.")
            return None
        time_series_data = data[time_series_key]
    elif 'Time Series (Daily)' in data:
        time_series_data = data['Time Series (Daily)']
    elif 'Weekly Time Series' in data:
        time_series_data = data['Weekly Time Series']
    elif 'Monthly Time Series' in data:
        time_series_data = data['Monthly Time Series']
    else:
        print(f"Error: {function} data not found in API response.")
        return None
    
    if function.startswith('TIME_SERIES_INTRADAY'):
        filtered_data = {datetime_key: values for datetime_key, values in time_series_data.items()
                         if start_date <= datetime_key.split()[0] <= end_date}
    else:
        filtered_data = {date: values for date, values in time_series_data.items()
                         if start_date <= date <= end_date}
    
    if not filtered_data:
        print(f"No data found for {symbol} within the given date range. Please try a different date range.")
        return None
    
    return filtered_data

#Graph
def generate_graph(data, chart_type):
    dates = list(data.keys())
    prices = [float(data[date]['4. close']) for date in dates]
    
    plt.figure(figsize=(10, 6))
    if chart_type == 'line':
        plt.plot(dates, prices, label='Close Price')
    elif chart_type == 'bar':
        plt.bar(dates, prices, color='skyblue', label='Close Price')
    elif chart_type == 'scatter':
        plt.scatter(dates, prices, color='red', label='Close Price')
    
    plt.title('Stock Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

#User Interface
def main():
    
    symbol = input("Enter the stock symbol: ").upper()
    
    print("Select the time series function:")
    print("1. Daily (TIME_SERIES_DAILY)")
    print("2. Weekly (TIME_SERIES_WEEKLY)")
    print("3. Monthly (TIME_SERIES_MONTHLY)")
    print("4. Intraday (TIME_SERIES_INTRADAY)")
    function_choice = input("Enter your choice (1/2/3/4): ")

    #Input for intraday interval selection
    interval = None
    if function_choice == '1':
        function = 'TIME_SERIES_DAILY'
    elif function_choice == '2':
        function = 'TIME_SERIES_WEEKLY'
    elif function_choice == '3':
        function = 'TIME_SERIES_MONTHLY'
    elif function_choice == '4':
        function = 'TIME_SERIES_INTRADAY'
        print("Select the intraday interval:")
        print("1. 1min")
        print("2. 5min")
        print("3. 15min")
        print("4. 30min")
        print("5. 60min")
        interval_choice = input("Enter your choice (1/2/3/4/5): ")
        intervals = {'1': '1min', '2': '5min', '3': '15min', '4': '30min', '5': '60min'}
        interval = intervals.get(interval_choice, None)
        if interval is None:
            print("Invalid interval choice. Please select 1, 2, 3, 4, or 5.")
            return
    else:
        print("Invalid choice. Please select 1, 2, 3, or 4.")
        return
    
    start_date = input("Enter the beginning date in YYYY-MM-DD format: ")
    end_date = input("Enter the end date in YYYY-MM-DD format: ")
    chart_type = input("Enter the chart type (line/bar/scatter): ").lower()
    
    if start_date > end_date:
        print("Error: End date cannot be before the beginning date.")
        return

    #Hold API key for Alpha Vantage
    api_key = "VHI1NLV7FLZATH71"
    
    stock_data = get_stock_data(symbol, function, start_date, end_date, api_key, interval)
    if stock_data is None:  # Updated handling for when no data is found
        print("Exiting the program. Please try again with a different date range.")
        return
    generate_graph(stock_data, chart_type)

if __name__ == "__main__":
    main()
