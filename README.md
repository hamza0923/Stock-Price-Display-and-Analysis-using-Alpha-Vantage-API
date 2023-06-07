# Stock Prices Analysis with GUI

This project allows you to analyze historical stock prices using the Alpha Vantage API and visualize the data in a graphical user interface (GUI) built with Tkinter. You can select a stock from a dropdown menu, view its closing prices over time, and perform linear regression analysis to predict future stock prices.

## Prerequisites

To run this project, you need to have the following:

- Python 3 installed on your system
- Required Python packages: `tkinter`, `requests`, `numpy`, `scikit-learn`, `matplotlib`

## Setup

1. Download the source code files.
2. Install the required Python packages by running the following command: "pip install [PACKAGE NAME]"
3. Obtain an API key from the Alpha Vantage website (https://www.alphavantage.co/). Sign up for a free account and get your API key.
4. Update the `API_KEY` variable in the `main.py` file with your API key.

## Usage

Run the `main.py` file to launch the GUI:

The GUI window will open, and you can interact with it as follows:

1. Select a stock from the dropdown menu.
2. The GUI will display the latest volume, open price, and close price for the selected stock.
3. The GUI will plot the closing prices of the selected stock over time.
4. Click the "Analyze" button to perform linear regression analysis on the stock's historical data and predict the next day's closing price.
5. The GUI will display the predicted closing price and the root mean square error (RMSE) of the regression model.

Note: The GUI will only display data for stocks selected. If a stock is not selected, the GUI will show "Selected Stock: NONE".

##AUTHOR: Hamza Imran
          Capital University of Science and Technology, Islamabad
