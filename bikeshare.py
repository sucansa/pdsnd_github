import pandas as pd
import numpy as np

# 3 Datasets to analyse: 
# Datasets are in csv format. Later this will be added in .gitignore file
# Following city datasets: Chicago, Washington and New York City are loaded into the CITY_DATA dictionary.

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
"""
Ask for the input from the user until correct input is given
Available options are chicago, new york city and washington

"""
while True:
    try:
        cit = input('Enter the city for which you would like to see the usage:\n Available options: chicago,new york city,washington \n')
        city = cit.lower()
        if city.lower() in CITY_DATA[city]:
            df = pd.read_csv(CITY_DATA[city])
    except KeyError:
        print('Please enter correct input- \n chicago,new york city,washington')
        continue
    else:
        break
#This section is to convert the dataframe to datetime format

df['Start Time'] = pd.to_datetime(df['Start Time'])
df['month'] = df['Start Time'].dt.month
df['day_of_week'] = df['Start Time'].dt.weekday_name
df['hour'] = df['Start Time'].dt.hour


"""
Function to find the popular or most used by people

Parameters:
Accept the Column name from the data frame for which the usage is calculated

Returns:
Returns the most used item from the column passed as a parameter

"""


def pop_item(inp):
    pop = df[inp].mode()[0]
    return pop

#To find the popular month- call the function pop_item(inp)
pop_month = pop_item('month')

#To display the maximum total count of the item
pop_month_ct = df['month'].value_counts().max()


month_list = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
for i in month_list.keys():
    if i == pop_month:
        print('The most popular month when the bicycle is rented more in {} is : '.format(city), month_list[i])
        print('Number of times rented in the popular month {} is: '.format(month_list[i]), pop_month_ct)

#to find the popular week- call the function pop_item(inp)
pop_week = pop_item('day_of_week')
pop_week_ct = df['day_of_week'].value_counts().max()
print('The most popular day when the bicycle is rented more in {} is : '.format(city),pop_week)
print('Number of times rented in the popular day {} is: '.format(pop_week),pop_week_ct)

#to find the popualr hour- call the function pop_item(inp)
pop_hour = pop_item('hour')
pop_hr_ct = df['hour'].value_counts().max()
print('The most popular hour when the bicycle is rented more in {} is : '.format(city),pop_hour)
print('Number of times rented in the popular hour {} is: '.format(pop_hour), pop_hr_ct)

#to find the most popular stations- call the function pop_item(inp)
SStation = pop_item('Start Station')
print('The most popular Start Station is: ', SStation) 
EStation = pop_item('End Station')
print('The most popular End Station is: ', EStation)

#to find the most popular trip- call the function pop_item(inp)
pop_trip = df.groupby(['Start Station','End Station'])
res = pop_trip['Trip Duration'].count().idxmax()
print('The most popular trip is : ', res)
df_filtered = df[(df['Start Station'] == res[0]) & (df['End Station'] == res[1])]

#to find the total trip duration
print('The total trip duration for the popular trip is (minutes): ',df_filtered['Trip Duration'].sum())

#to find the average travel time for the popular trip
print('The average travel time for the popular trip is (minutes): ',df_filtered['Trip Duration'].mean())


"""
Function to find the total count group wise

Parameters- The column name for which the count is needed is passed

Returns the total counts calculated group wise. 
If no data is present for a group, it is displayed as 'NaN'
"""

def val_ct(col_name):
    val = df_filtered[col_name].value_counts(dropna = False)
    return val

#to find the user type, Gender and YOB counts for the popular trip
#-call the function val_ct(col_name)

try:
    usr_typ = val_ct('User Type')
    print(usr_typ)
    gender_typ = val_ct('Gender')
    print(gender_typ)
    eyob = df_filtered['Birth Year'].min()
    print('The Earliest year of birth: ',eyob )
    ryob = df_filtered['Birth Year'].max()
    print('The Recent year of birth: ',ryob)
    cyob = df_filtered['Birth Year'].mode()[0]
    print('The common year of birth: ',cyob)
except KeyError as e:
    print(e, 'data not available \n')


"""
Get user input to display the statistics for which month

Available inputs are from January to June, as the data is available only for these months

Prompts for input until the user gives the right input

"""
month_list = ['january','february','march','april','may','june']
i = 0
while i < len(month_list):
    op = input('Enter the month name for which you would like to see the statistics between January to June \n')
    opt= op.lower()
    try:
        opt = month_list.index(opt) + 1
        if i == opt:
            df = df[df['month'] == opt]                           
        break
    except Exception as e:        
        print('Incorrect Input or data not available for the month',e )
        continue
"""
Get user input to display the statistics for which day

Available inputs are from Sunday to Saturday

Prompts for input until the user gives the right input

"""

day_list = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
j = 0
while j < len(day_list):
    op1 = input('Enter the day for which you would like to view the data \n')
    inp = op1.lower()
    try:
        inp = day_list.index(inp)
        if j == inp:
            df = df[df['day_of_week'] == day_list[j].title()]
        break
    except Exception as e:
        print('Incorrect input given', e)
        continue
"""
Get user input to display the raw 5 lines of data

If user gives yes, first 5 lines are displayed. 
Again prompts for user confirmation to displaythe next set.

Prompts for user input until the user enters no

"""
usr_inp = input('Would you like to see 5 lines of raw data? y/n \n')
if usr_inp in ('y','Y','yes','Yes'):
   for i in range(0,len(df),5):
       print(df[i:i+5])
       inp_ag = input('Would you like to see the next set of 5 rows? y/n \n')
       if inp_ag in ('y','yes','Y','YES','Yes'):
           continue
       elif inp_ag in ('n','no','N','NO','No'):
           print('Thanks! Code complete')
           break
else:
    print('Code Complete')

