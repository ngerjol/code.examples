import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['overweight'] = df['weight'] / ((df['height'] / 100)**2)
df.loc[df["overweight"] <= 25, "overweight"] = 0
df.loc[df["overweight"] > 25, "overweight"] = 1
df["overweight"]=df["overweight"].astype(int)
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df.loc[df["cholesterol"] == 1, "cholesterol"] = 0
df.loc[df["cholesterol"] > 1, "cholesterol"] = 1
df.loc[df["gluc"] == 1, "gluc"] = 0
df.loc[df["gluc"] > 1, "gluc"] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=["cholesterol","gluc", "smoke", "alco", "active", "overweight"])
   

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(df_cat.columns.tolist(), as_index=False).size()
    df_cat = df_cat.rename({"size" : "total"}, axis = 1)
  

    # Draw the catplot with 'sns.catplot()'
    plot = sns.catplot(data=df_cat, x="variable", y="total", col="cardio", hue="value", kind="bar")
    print(plot)

    # Get the figure for the output
    fig = plot.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) &(df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975)) ]
   
    
    # Calculate the correlation matrix
    corr = df_heat.corr()
    
    # Generate a mask for the upper triangle
    mask = np.triu(corr)
   
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize = (9,7))

    # Draw the heatmap with 'sns.heatmap()'
    heat = sns.heatmap(corr, vmin=-.16, vmax=.32, center=0, annot = True, mask=mask, linewidths=0.5, fmt = ".1f", cbar_kws={"shrink": 0.5, "ticks":[-0.08, 0.00, 0.08, 0.16, 0.24]})
    print(heat)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
