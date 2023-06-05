import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
   
   
    fig = plt.figure()
    fig.set_figwidth(20)
    fig.set_figheight(6)
    plot = plt.plot(df.index.values, df['value'], color='red')
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")

  
    fig=fig.figure
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png') 
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    plt.close()
    df_bar = df.resample("MS").mean().round().astype(int)
    df_bar["month"] = df_bar.index.month
    df_bar["year"] = df_bar.index.year
    print(df_bar.head())
    df_bar = df_bar.pivot(index='year', columns="month")['value']
    df_bar.reset_index()
    print(df_bar.head())
    df_bar.columns = ["January", "February", "March", "April",  "May",  "June",  "July", "August",  "September", "October",  "November", "December"]
    df_bar["year"] = df_bar.index
    print(df_bar.head())


    # Draw bar plot
    fig = df_bar.plot(x="year", kind="bar", stacked=False)
  
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title='Months')

    fig=fig.figure
    fig.set_figwidth(12)
    fig.set_figheight(10)
   


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    plt.close()
    fig=plt.figure(figsize=(15,10))
    ax1 = fig.add_subplot(1,2,1)
    sns.boxplot(x=df_box["year"], y=df_box["value"])
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")
    ax1.set_title("Year-wise Box Plot (Trend)")
  
    ax2 = fig.add_subplot(1,2,2)
    sns.boxplot(x=df_box["month"], y=df_box["value"], order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    ax2.set_title("Month-wise Box Plot (Seasonality)")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
