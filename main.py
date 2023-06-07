# A GUI APP FOR STOCK PRICE DISPLAY AND ANALYSIS USING ALPHA VANTAGE API
# AUTHOR: HAMZA IMRAN
# Github: https://github.com/hamza0923/Stock-Price-Display-and-Analysis-using-Alpha-Vantage-API

from tkinter import Button, Label, Tk, ttk, Frame
import requests
import csv
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from math import sqrt

API_KEY = "API KEY" # Replace with your own api
# ---------------------------------------API-------------------------------------------
CSV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    stock_names = []
    for row in my_list:
        symbol = row[0]
        name = row[1]
        stock_name = f"{symbol} - {name}"
        stock_names.append(stock_name)
        print(stock_name)

#====================================
color1 = "#ececec"
color2 = "#3E00FF"
color3 = "#AE00FB"
color4 = "#B5FFD9"

def stock_analysis(dates, opening_prices, closing_prices, volumes):
    print("Analyzing...")
    # Convert dates to the number of days since a reference date
    reference_date = datetime.strptime(dates[0], "%Y-%m-%d")
    numeric_dates = [(datetime.strptime(date, "%Y-%m-%d") - reference_date).days for date in dates]

    # Prepare the data
    X = np.column_stack((numeric_dates[:-1], closing_prices[:-1], volumes[:-1], opening_prices[:-1]))
    y = np.array(closing_prices[1:])  # Target variable shifted by one day

    # Split the data into training and test sets
    train_size = int(0.85 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_predicted = model.predict(X_test)

    rmse = sqrt(mean_squared_error(y_test, y_predicted))
    print("RMSE:", rmse)

    # Make predictions for tomorrow's price
    tomorrow_features = np.array([numeric_dates[-1] + 1, closing_prices[-1], volumes[-1], opening_prices[-1]]).reshape(1, -1)
    predicted_price = model.predict(tomorrow_features)

    prediction = f"Predicted close price for tomorrow is {round(predicted_price[0], 3)}"
    print(prediction)
    analysis_result.config(text=prediction + f"\nRMSE: {round(rmse, 5)}")

def plot_stock_data(stock_symbol):
    # Making a new frame for the graph and toolbar
    global graph_frame
    graph_frame = Frame(window)
    graph_frame.grid(row=5, column=0, columnspan=2)

    # Making a new figure to display in tkinter
    fig = Figure(figsize=(11, 5))
    plot = fig.add_subplot(111)
    plot.set_title("NONE")

    # Displaying the graph
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    # Creating and displaying a toolbar
    toolbar = NavigationToolbar2Tk(canvas, graph_frame)
    toolbar.update()
    toolbar.pack(side='bottom', fill='x')

    if stock_symbol != " ":
        # API endpoint for retrieving the historical stock data
        API_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock_symbol}&outputsize=full&apikey={API_KEY}"

        # Send a GET request to the Alpha Vantage API
        response = requests.get(API_URL)
        data = response.json()

        # Extract the historical price data from the response
        time_series = data["Time Series (Daily)"]
        dates = sorted(time_series.keys())
        closing_prices = [float(time_series[date]["4. close"]) for date in dates]
        volumes = [float(time_series[date]["6. volume"]) for date in dates]
        opening_prices = [float(time_series[date]["1. open"]) for date in dates]

        # Display the relevant data
        stock_selected_volume.config(text="Volume: " + str(volumes[len(volumes)-1]), font=('open sans', 10, 'bold'))
        stock_selected_open_price.config(text="Open Price: " + str(opening_prices[len(opening_prices)-1]), font=('open sans', 10, 'bold'))
        stock_selected_close_price.config(text="Close Price: " + str(closing_prices[len(closing_prices)-1]), font=('open sans', 10, 'bold'))


        # Making the graph with required data
        plot.plot(dates, closing_prices)
        plot.set_xlabel("Date")
        plot.set_ylabel("Closing Price")
        plot.set_title("Selected Stock: " + stock_symbol)
        plot.grid(True)


        plot.set_xlim(len(dates)-50, len(dates)-1)  # Displaying last 50 data elements
        plot.set_xticklabels(dates, rotation=45)
        fig.subplots_adjust(bottom=0.2, hspace=0.4)             # Adding some bottom margin for rotated dates

        analyze_button.config(command=lambda: stock_analysis(dates, opening_prices, closing_prices, volumes))


def stock_selection_handler(event):
    selected_stock = stocks_dropdown.get()
    split_name = selected_stock.split("-")
    stock_symbol = split_name[0].strip(" ")
    #stock_selected.config(text="Selected Stock: " + stock_symbol)
    graph_frame.grid_forget()
    plot_stock_data(stock_symbol)


# -----------------------------------GUI WINDOW-------------------------------------------
window = Tk()
window.title("Stock Market - Alpha Vantage API")
window.geometry("1100x840")
#window.resizable(width=False, height=False)

title = Label(text="Stock Market", foreground=color3, font=('open sans', 26, 'bold'))
title.grid(row=0, column=0, sticky='w', padx=10, pady=10)
border_bottom = Frame(window, width=1100, height=1, background=color3)
border_bottom.grid(row=1, column=0, columnspan=2, sticky='ew')

stocks_label = Label(text="Stock", foreground=color2, font=('open sans', 16, 'bold'))
stocks_label.grid(row=2, column=0, sticky='w', padx=5, pady=10)
stocks_dropdown = ttk.Combobox(width=25, font=("open sans", 12))
stocks_dropdown['values'] = stock_names
stocks_dropdown.grid(row=2, column=0, padx=(0, 640))
stocks_dropdown.bind("<<ComboboxSelected>>", stock_selection_handler)
border_bottom = Frame(window, width=1100, height=1, background=color3)
border_bottom.grid(row=3, column=0, columnspan=2, sticky='n')


stock_data = Frame(width=1100, height=70, background=color1)
stock_data.grid(row=4, column=0)

#stock_selected = Label(stock_data, text="Selected Stock: NONE", foreground=color2, font=('open sans', 14, 'bold'))
#stock_selected.grid(row=0, column=0, columnspan=3, sticky='nw', padx=(0, 500))

stock_selected_volume = Label(stock_data, text="Volume: 0.000", foreground=color2, font=('open sans', 10))
stock_selected_volume.grid(row=0, column=3, sticky="e", padx=(650, 0), pady=15)
stock_selected_open_price = Label(stock_data, text="Open Price: 0.000", foreground=color2, font=('open sans', 10))
stock_selected_open_price.grid(row=0, column=4, sticky="e")
stock_selected_close_price = Label(stock_data, text="Close Price: 0.000", foreground=color2, font=('open sans', 10))
stock_selected_close_price.grid(row=0, column=5, sticky="e")


plot_stock_data(" ")

analyze_button = Button(text="Analyze", width=15, pady=1, font=('open sans', 14))
analyze_button.grid(row=7, column=0)

analysis_result = Label(text="..", foreground=color3, font=('open sans', 13))
analysis_result.grid(row=8, column=0)
window.mainloop()



