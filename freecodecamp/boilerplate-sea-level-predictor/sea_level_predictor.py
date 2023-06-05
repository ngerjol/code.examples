import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv("epa-sea-level.csv")
    
    # Create scatter plot
    fig, ax = plt.subplots()
    plt.scatter(df['Year'], df["CSIRO Adjusted Sea Level"])
  
    
  
    # Create first line of best fit
    res = linregress(df["Year"],df["CSIRO Adjusted Sea Level"])
    x = list(range(1880,2051))
    num = pd.DataFrame({'x': x})
    plt.plot(num, res.intercept + res.slope * num, 'r', label = "first line of fit")


    # Create second line of best fit
    df = df[df["Year"] >= 2000]
    res2 = linregress(df["Year"],df["CSIRO Adjusted Sea Level"])
    x = list(range(2000,2051))
    num = pd.DataFrame({'x': x})
    plt.plot(num, res2.intercept + res2.slope * num, 'r', label = "second line of fit")


    # Add labels and title
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.title("Rise in Sea Level")
  
    fig=fig.figure
    fig.set_figwidth(12)
    fig.set_figheight(10)

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()