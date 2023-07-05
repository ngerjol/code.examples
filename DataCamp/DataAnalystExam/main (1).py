import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
#import data
df = pd.read_csv('food_claims_2212.csv')

#Task 1
#For every column in the data:
# a. State whether the values match the description given in the table above
# b. state the number of missing values in the columns
# c. Descrive what you did to make values match the description if they did not match. 

#Identifying Columns

## claim ID
#print(df.claim_id.describe()) #summary stats for my info
#bool = pd.isnull(df['claim_id'])
#print(df[bool]) # this shows there are no missing values
#print(df['claim_id'].nunique()) #shows 2000 unique

## time to close
#print(df.time_to_close.describe())
#bool = pd.isnull(df['time_to_close'])
#print(df[bool]) #this shows there are no missing values
#print(df['time_to_close'].nunique()) #this shows there are 256 unique values

##claim amount
#print(df.claim_amount.describe())
#print(df.claim_amount.head())
df['claim_amount'] = df['claim_amount'].replace({r'R\$ ':''}, regex = True)
df['claim_amount'] = pd.to_numeric(df['claim_amount'])
#print(df.claim_amount.describe())
#print(df.claim_amount.head())
bool = pd.isnull(df['claim_amount'])
#print(df[bool])  #shows no missing values
#print(df['claim_amount'].nunique()) #this shows there are 2000 unique values

##amount paid
#print(df.amount_paid.describe())
#bool = pd.isnull(df['amount_paid'])
#print(df[bool])  #shows 36 missing values
#print(df['amount_paid'].nunique()) #this shows there are 1963 unique values
df['amount_paid'] = df['amount_paid'].fillna(df['amount_paid'].median())
#replaceing nulls with median value
## checking for nulls again to verify above worked
#bool = pd.isnull(df['amount_paid'])
#print(df[bool])
#test = df[bool]
#print(test['amount_paid']) #double checking nulls were replaced
#print(df['amount_paid'].nunique())

##location
#print(df.location.describe())
#print(df.location.head())
#bool = pd.isnull(df['location'])
#print(df[bool])  #shows no missing values
#print(df['location'].nunique()) #this shows there are 4 unique values

##individuals on claim
#print(df.individuals_on_claim.describe())
#bool = pd.isnull(df['individuals_on_claim'])
#print(df[bool])  #shows no missing values
#print(df['individuals_on_claim'].nunique()) #this shows there are 15 unique values

##linked cases
#bool = pd.isnull(df['linked_cases'])
#print(df[bool])  #shows 26 missing values
#print(df['linked_cases'].nunique()) #this shows there are 2 unique values
df['linked_cases'] = df['linked_cases'].fillna(False) #replacing nulls with false
#test = df[bool]
#print(test['linked_cases']) #double checking nulls were replaced

##cause
#bool = pd.isnull(df['cause'])
#print(df[bool])  #shows no missing values
#print(df['cause'].nunique()) #this shows there are 5 unique values
#print(df['cause'].unique()) #check what the mistaken values where
#print(df.query("cause==' Meat'")["location"]) #identify locations of this mistake
#print(df.query("cause=='VEGETABLES'")["location"]) #identify locations of this mistake
df = df.replace({'cause' : {' Meat' : 'meat', 'VEGETABLES': 'vegetable'}})
#print(df['cause'].nunique())# checking replacement worked
#print(df['cause'].unique())

#task 2
#Create a visualization that shows the number of claims in each location. Use the Visualization to:
#a. State which category of the variable location has the most observations
#b. Explain whether the observations are balanced across catagories of the varaible location. 


#Rework the data to make it graphable
df2 = df.groupby(['location'])['claim_id'].agg('count').sort_values().reset_index()
df2.rename(columns={'claim_id':'number_of_observations'}, inplace=True)
#print(df2) to get the totals

# Draw the catplot with 'sns.catplot()'
sns.set_style("darkgrid")
plot = sns.catplot(data=df2, x="location", y='number_of_observations', kind="bar", height=4, aspect=1)
plot.set(xlabel='Location',
       ylabel='Number of Observations',
       title='Customer Claims by Location', yticks = [100, 200, 300, 400, 500, 600, 700, 800, 900])
plot.figure.subplots_adjust(top=.90)
plt.suptitle('         Recife has the most claims by location', y=.9, fontsize=6)


# Get the figure for the output
fig = plot.fig



# Save the figure
fig.savefig('claims_by_location.png')

#task 3
#Describe the distribution of time to close for all claims. Your answer must include a visualization that shows the distriburtion. 

#print(df['time_to_close'].describe()) # get the summary statistics
#Used to find the number of outliers below 89 and above 273
dftest = df['time_to_close'] > 273
dfoutlier = df[dftest]
dfoutlier = dfoutlier.drop(columns=['claim_id'])
#print(dfoutlier)

#print(dfoutlier.claim_amount.describe()) #mean:51187.41, min: 20323, Q1%: 39187, median: 50945.9, Q3: 62212.265, Max: 75253
#print(df.claim_amount.describe()) #mean 27156, min, 1637, Q1: 13758, median, 24821, Q3: 38581, Max: 76106

#print(dfoutlier.amount_paid.describe()) #mean: 37931, min:17625, Q1: 28732, Median: 37635, Q3: 47788.83, max: 52478
#print(df.amount_paid.describe())# mean: 21516, min: 1516, Q1: 11106, Median: 20105, Q3: 30472, MAX: 52498.75

#print(dfoutlier.linked_cases.value_counts()) # all linked cases are false

#print(dfoutlier.individuals_on_claim.value_counts()) # 6 or more inviduals on claim, increasing in number as the individuals increase, 99 of these 114 are when individuals are 10 or more
#print(dfoutlier.individuals_on_claim.value_counts() / df.individuals_on_claim.value_counts() * 100) #for values 6-15 respectivly, .913% 1.316%, 3.247%, 4.930%, 6.66%, 8.76%, 10.256%, 11.510%, 18.182%, 24.242%

#print(dfoutlier.cause.value_counts()) #78 unknown, 38 meat, 2 vegetable
#print(dfoutlier.cause.value_counts() / df.cause.value_counts() * 100)#3.97% of meats, 10.4% of unknowns, .6% of vegetable

#location
#print(dfoutlier.location.value_counts()) #recife 48, sao luis 38, natal 15, fortaleza 13
#print(dfoutlier.location.value_counts() / df.location.value_counts() * 100) #4.18% of fortalezas claims are outliers, 5.23% of natals claims are outliers, 5.42% of Reciefs claims ar eoutliers, 7.35% of sao luis claims are outliers. 

#create boxplot with scattered backdrop 
fig, ax = plt.subplots()

#create boxplot
plt.boxplot(df["time_to_close"], vert=False, showmeans=True,  manage_ticks=True, showfliers=False, whiskerprops = dict(linewidth=2.0), medianprops= dict(linewidth=2.0, color = 'blue'), widths = .25)
#print([item.get_xdata(1) for item in B['whiskers']]) # [158, 89] [204,273]

#create scatter
x = df["time_to_close"]
 # Add some random "jitter" to the x-axis
y = np.random.normal(1, 0.01, size=len(x))
plt.plot(x, y, 'r.', alpha=0.25)

#Make it look nice
plt.ylabel(None)
plt.xlabel("Number of days", fontsize = 20)
plt.title("Time to close claims", fontsize= 25)
plt.yticks([1], [''])
plt.xticks([50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550], fontsize = 15)
  
fig=fig.figure
fig.set_figwidth(20)
fig.set_figheight(8)

# Save plot 
plt.savefig('time_to_close_box.png')
plt.clf()

#histogram 
w=1
#df3 = df[(np.abs(stats.zscore(df['time_to_close'])) < 3)] removes outliers
plt.hist(x = 'time_to_close', data=df, edgecolor='black', bins=np.arange(min(df['time_to_close']), max(df['time_to_close']) + w, w))
plt.ylabel("Count")
plt.xlabel("Time in Days", fontsize = 20)
plt.title("Time to close claims", fontsize= 25)
plt.xticks([0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525], fontsize = 15)
fig=fig.figure
fig.set_figheight(15)
plt.savefig('time_to_close_histogram')

## creating data for tables

tab_loc_val = dfoutlier.location.value_counts()
tab_loc_tot = dfoutlier.location.value_counts() / len(dfoutlier.index) * 100
tab_loc_per = dfoutlier.location.value_counts() / df.location.value_counts() * 100
tab_loc_full = df.location.value_counts() / 2000 * 100

tab_cause_val = dfoutlier.cause.value_counts()
tab_cause_tot = dfoutlier.cause.value_counts() / len(dfoutlier.index) * 100
tab_cause_per = dfoutlier.cause.value_counts() / df.cause.value_counts() * 100

tab_ind_val = dfoutlier.individuals_on_claim.value_counts()
tab_ind_val = tab_ind_val.sort_values()
tab_ind_tot = dfoutlier.individuals_on_claim.value_counts() / len(dfoutlier.index) * 100
tab_ind_tot = tab_ind_tot.sort_values()
tab_ind_per = dfoutlier.individuals_on_claim.value_counts() / df.individuals_on_claim.value_counts() * 100
tab_ind_per = tab_ind_per.dropna()

#print(tab_ind_val)
#print(tab_ind_val.iat[0]) #first indecies value
#print(tab_ind_val.index[0]) # first index
#print(tab_cause_val)
#print(tab_cause_per)


## create cause table
title_text = 'Outliers by Cause'
#footer_text = ''
fig_background_color = 'white'
fig_border = 'white'
data =  [
            [tab_cause_val.index[0], tab_cause_val.index[1], tab_cause_val.index[2]],
            [ '# of outliers',  tab_cause_val.iat[0], tab_cause_val.iat[1],   tab_cause_val.iat[2]],
            ['% of total outliers', tab_cause_tot.iat[0], tab_cause_tot.iat[1],   tab_cause_tot.iat[2]],
            ['% outlier of total claim',  tab_cause_per.iat[0], tab_cause_per.iat[1],   tab_cause_per.iat[2]],
        ]
# Pop the headers from the data array
column_headers = data.pop(0)
row_headers = [x.pop(0) for x in data]
# Table data needs to be non-numeric text. Format the data
# while I'm at it.
cell_text = []
for row in data:
    cell_text.append([f'{x/1:1.2f}' for x in row])
# Get some lists of color specs for row and column headers
rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
# Create the figure. Setting a small pad on tight_layout
# seems to better regulate white space. Changed figsize to remove bluespace.
plt.figure(linewidth=2,
           edgecolor=fig_border,
           facecolor=fig_background_color,
           tight_layout={'pad':1},
           figsize=(5,2)
          )
# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')
# Scaling is the only influence we have over top and bottom cell padding.
# Make the rows taller (i.e., make cell y scale larger).
the_table.scale(1, 1.5)
# Hide axes
ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
# Hide axes border
plt.box(on=None)
# Add title
plt.suptitle(title_text)
# Add footer
#plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
# Force the figure to update, so backends center objects correctly within the figure.
# Without plt.draw() here, the title will center on the axes and not the figure.
plt.draw()
# Create image. plt.savefig ignores figure edge and face colors, so map them.
fig = plt.gcf()
plt.savefig('cause_table.png',
            #bbox='tight',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=150
            )
plt.clf()

## create location table
title_text = 'Outliers by Location'
#footer_text = ''
fig_background_color = 'white'
fig_border = 'white'
data =  [
            [tab_loc_val.index[0], tab_loc_val.index[1], tab_loc_val.index[2], tab_loc_val.index[3]],
            [ '# of outliers',  tab_loc_val.iat[0], tab_loc_val.iat[1],   tab_loc_val.iat[2], tab_loc_val.iat[3]],
            ['% of total outliers', tab_loc_tot.iat[0], tab_loc_tot.iat[1],   tab_loc_tot.iat[2], tab_loc_tot.iat[3]],
            ['% outlier of total claim',  tab_loc_per.iat[0], tab_loc_per.iat[1],   tab_loc_per.iat[2], tab_loc_per.iat[3]],
            ['% total claims processed at location', tab_loc_full[0], tab_loc_full[1], tab_loc_full[2], tab_loc_full[3]]
        ]
# Pop the headers from the data array
column_headers = data.pop(0)
row_headers = [x.pop(0) for x in data]
# Table data needs to be non-numeric text. Format the data
# while I'm at it.
cell_text = []
for row in data:
    cell_text.append([f'{x/1:1.2f}' for x in row])
# Get some lists of color specs for row and column headers
rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
# Create the figure. Setting a small pad on tight_layout
# seems to better regulate white space. Changed figsize to remove bluespace.
plt.figure(linewidth=2,
           edgecolor=fig_border,
           facecolor=fig_background_color,
           tight_layout={'pad':1},
           figsize=(6,2)
          )
# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')
# Scaling is the only influence we have over top and bottom cell padding.
# Make the rows taller (i.e., make cell y scale larger).
the_table.scale(1, 1.5)
# Hide axes
ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
# Hide axes border
plt.box(on=None)
# Add title
plt.suptitle(title_text)
# Add footer
#plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
# Force the figure to update, so backends center objects correctly within the figure.
# Without plt.draw() here, the title will center on the axes and not the figure.
plt.draw()
# Create image. plt.savefig ignores figure edge and face colors, so map them.
fig = plt.gcf()
plt.savefig('location_table.png',
            #bbox='tight',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=150
            )
plt.clf()

## create Individuals on claim table
title_text = 'Outliers by Individuals on Claim'
#footer_text = ''
fig_background_color = 'white'
fig_border = 'white'
data =  [
            [tab_ind_val.index[0], tab_ind_val.index[1], tab_ind_val.index[2], tab_ind_val.index[3], tab_ind_val.index[4], tab_ind_val.index[5], tab_ind_val.index[6], tab_ind_val.index[7], tab_ind_val.index[8], tab_ind_val.index[9]],
            [ '# of outliers',  tab_ind_val.iat[0], tab_ind_val.iat[1],   tab_ind_val.iat[2],   tab_ind_val.iat[3],   tab_ind_val.iat[4],   tab_ind_val.iat[5],   tab_ind_val.iat[6],   tab_ind_val.iat[7],   tab_ind_val.iat[8],   tab_ind_val.iat[9]],
            ['% of total outliers', tab_ind_tot.iat[0], tab_ind_tot.iat[1],   tab_ind_tot.iat[2],   tab_ind_tot.iat[3],   tab_ind_tot.iat[4],   tab_ind_tot.iat[5],   tab_ind_tot.iat[6],   tab_ind_tot.iat[7],   tab_ind_tot.iat[8],   tab_ind_tot.iat[9]],
            ['% outlier of total claim',  tab_ind_per.iat[0], tab_ind_per.iat[1],   tab_ind_per.iat[2],   tab_ind_per.iat[3],   tab_ind_per.iat[4],   tab_ind_per.iat[5],   tab_ind_per.iat[6],   tab_ind_per.iat[7],   tab_ind_per.iat[8],   tab_ind_per.iat[9]]
        ]
# Pop the headers from the data array
column_headers = data.pop(0)
row_headers = [x.pop(0) for x in data]
# Table data needs to be non-numeric text. Format the data
# while I'm at it.
cell_text = []
for row in data:
    cell_text.append([f'{x/1:1.2f}' for x in row])
# Get some lists of color specs for row and column headers
rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
# Create the figure. Setting a small pad on tight_layout
# seems to better regulate white space. Changed figsize to remove bluespace.
plt.figure(linewidth=2,
           edgecolor=fig_border,
           facecolor=fig_background_color,
           tight_layout={'pad':1},
           figsize=(5,2)
          )
# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=row_headers,
                      rowColours=rcolors,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=column_headers,
                      loc='center')
# Scaling is the only influence we have over top and bottom cell padding.
# Make the rows taller (i.e., make cell y scale larger).
the_table.scale(1, 1.5)
# Hide axes
ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
# Hide axes border
plt.box(on=None)
# Add title
plt.suptitle(title_text)
# Add footer
#plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6, weight='light')
# Force the figure to update, so backends center objects correctly within the figure.
# Without plt.draw() here, the title will center on the axes and not the figure.
plt.draw()
# Create image. plt.savefig ignores figure edge and face colors, so map them.
fig = plt.gcf()
plt.savefig('IoC_table.png',
            #bbox='tight',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=150
            )
plt.clf()

## Task 4
# Describe the relationship between time to close and location. Your answer must include a visualization to demonstrate the relationship. 

#change the data to graph
df_temp = df['location'] == 'RECIFE'
df_loc_1 = df[df_temp]
df_loc_1 = df_loc_1.drop(columns=['claim_id', 'claim_amount', 'amount_paid', 'individuals_on_claim', 'linked_cases', 'cause']).reset_index()

df_temp = df['location'] == 'SAO LUIS'
df_loc_2 = df[df_temp]
df_loc_2 = df_loc_2.drop(columns=['claim_id', 'claim_amount', 'amount_paid', 'individuals_on_claim', 'linked_cases', 'cause']).reset_index()

df_temp = df['location'] == 'NATAL'
df_loc_3 = df[df_temp]
df_loc_3 = df_loc_3.drop(columns=['claim_id', 'claim_amount', 'amount_paid', 'individuals_on_claim', 'linked_cases', 'cause']).reset_index()

df_temp = df['location'] == 'FORTALEZA'
df_loc_4 = df[df_temp]
df_loc_4 = df_loc_4.drop(columns=['claim_id', 'claim_amount', 'amount_paid', 'individuals_on_claim', 'linked_cases', 'cause']).reset_index()
#plot the box plots
# Set the figure size
plt.rcParams["figure.figsize"] = [12.50, 10.50]
plt.rcParams["figure.autolayout"] = True
plt.rcParams.update({'font.size': 15})

# Pandas dataframe
data = pd.DataFrame({"Recife": df_loc_1['time_to_close'], "Sao Luis": df_loc_2['time_to_close'], "Natal": df_loc_3['time_to_close'], "Fortaleza": df_loc_4['time_to_close']})

# Plot the dataframe
ax = data[['Recife', 'Sao Luis', 'Natal', 'Fortaleza']].plot(kind='box', title='Time to close by location')

plt.yticks([75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525])

plt.ylabel('Time to close claims')
plt.xlabel("Location")
# Display the plot

fig=fig.figure

# Save plot 
plt.savefig('location_box_plots')
plt.clf()