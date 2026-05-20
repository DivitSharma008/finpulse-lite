# finpulse-lite

This project uses pandas and matplotlib.pyplot to analyse the data.
yfinance is used to fetch the data about each stock and is stored into a seperate CSV file
The same is being done for 10 different stocks
Now plots consisting of close prices and moving averages is stored for each stock

Run the download_data.py file first to store the data into each csv file.
Store these in the data folder

Run plot_stock.py and save all the charts into a local folder named images.

A sample chart of INFY is as follows:
<img width="1366" height="655" alt="INFY_chart" src="https://github.com/user-attachments/assets/25215e19-76d5-468e-8f9b-fcf067f35033" />

I am using the SMA Crossover Strategy to determine when to buy or sell a stock
