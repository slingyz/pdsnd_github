import time
import pandas as pd
import numpy as np
from datetime import datetime

#from collections import Counter

def main():

    CITY_DATA = { 'chicago': 'chicago.csv',
                  'new york city': 'new_york_city.csv',
                  'washington': 'washington.csv' }


    #start of program after title, loop here if restarting program from the top

    #Bicycle Picture
    print(' o__         __o        ,__o        __o           __o\n ,>/_       -\<,      _-\_<,       _`\<,_       _ \<_\n(*)`(*).....O/ O.....(*)/\'(*).....(*)/ (*).....(_)/(_)')

    #Project Title
    print('                        ___       __                /                \n| | _  |  _  _ __  _     |  _    (_ _|_ _     _ __     _             \n|^|(/_ | (_ (_)|||(/_    | (_)   __) |_(/_\_/(/_| |   _>             \n _              __                _              _        o          \n|_) o  |  _    (_ |_  _  __ _    | \ _ _|_ _    |_) __ _  |  _  _ _|_\n|_) |  |<(/_   __)| |(_| | (/_   |_/(_| |_(_|   |   | (_)_| (/_(_  |_')

    #Welcome Statement
    print('\nHello! Welcome to Steven Ling\'s udacity python project! \nLet\'s explore some US bikeshare data!\n\n')

    #defining time intervals for display time function
    intervals = (
        ('years',217728000), # 60 * 60 * 24 * 7 * 30 * 12
        ('months',18144000), # 60 * 60 * 24 * 7 * 30
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
        )

    #function to convert seconds to years,months,weeks,days,hours,seconds
    def display_time(seconds, granularity=6):
        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])

    def get_filters():
        #City Choice Input
        city_choice = input("Which city are you interested in?\n\nChoose a city by entering the corresponding number:\n1 for Chicago or\n2 for New York city or\n3 for Washington?")
        global city
        if city_choice == '1':
            city ='chicago'
            print('you have chosen Chicago!\n')
        elif city_choice == '2':
            city = 'new york city'
            print('you have chosen New York city!\n')
        elif city_choice == '3':
            city = 'washington'
            print('you have chosen Washington city!\n')
        else:
            print('This does not seem to be a valid choice!')
            restart = input("Do you wish to reselect filters? y/n?\n").lower()
            if restart == 'y':
                get_filters()
            else:
                exit()

        # TO DO: get user input for month (all, january, february, ... , june)
        # Month Choice Input
        global month
        month =()
        month_choice = input("Which month are you interested in?\n\nChoose a month by entering the following choices:\n (all, january, february, march, april, may, june) ")
        valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month_choice = month_choice.lower()
        if month_choice in valid_months:
            month = month_choice
            print ('For months, you have selected {}'.format(month))
        else:
            print('This does not seem to be a valid choice!')
            restart_month = input("Do you wish to choose filters again? y/n?\n").lower()
            if restart_month == 'y':
                get_filters()
            else:
                exit()

        # Get user input for day of the week
        global day
        day=()
        day_choice = input("which day of the week are you interested in?\n\nChoose a day by entering the following choices:\n (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)")
        valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_choice = day_choice.lower()
        if day_choice in valid_days:
            day = day_choice
            print ('For days, you have selected {}'.format(day))
        else:
            print('This does not seem to be a valid choice!')
            restart_days = input("Do you wish to repick filters? y/n?\n").lower()
            if restart_days == 'y':
                get_filters()
            else:
                exit()
        print('-'*40)
        return city, month, day

    def load_data(city, month, day):
        # load data file into a dataframe
        global df
        df = pd.read_csv(CITY_DATA[city],index_col=0, infer_datetime_format=True)
        # convert the Start Time and end Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])

        # extract month and day of week from Start Time to create new columns
        df['Start_Hour']    = df['Start Time'].dt.hour
        df['month']         = df['Start Time'].dt.month
        df['day_of_week']   = df['Start Time'].dt.weekday_name
        df['Start Time']    = df['Start Time'].dt.time
        df['End Time']      = df['End Time'].dt.time
        
        # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

        return df

    def time_stats(df):
        #Displays statistics on the most frequent times of travel.
        print('\nCalculating The Most Frequent Times of Travel for: \n City:  {}\n Month: {}\n Day:   {}'.format(city,month,day))

        start_time = time.time()
        time_delay_long()
        #display the most common month
        most_common_month = df['month'].mode()[0]
        print('Most Common month: \n', most_common_month)

        #display the most common day of week
        most_common_day = df['day_of_week'].mode()[0]
        print('Most Common Day: \n', most_common_day)

        #display the most common start hour
        most_common_start_hour = df['Start_Hour'].mode()[0]
        print('Most Common Start Hour:\n', most_common_start_hour)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def station_stats(df):
        #Displays statistics on the most popular stations and trip.
        print('\nCalculating The Most Popular Stations and Trips for: \n City:  {}\n Month: {}\n Day:   {}'.format(city,month,day))

        start_time = time.time()
        time_delay_short()
        #display most commonly used start station
        most_common_start_station = df['Start Station'].mode()[0]
        print('Most Common Start Station:{}\n'.format(most_common_start_station))

        #print('Most Common Start Hour:', most_common_start_hour)
        most_common_start_hour = df['Start_Hour'].mode()[0]
        print('Most Common Start Hour:{}:  '.format(most_common_start_hour))

        #display most commonly used end station
        most_common_end_station = df['End Station'].mode()[0]
        print('Most Common End Station:{}: '.format(most_common_end_station))

        #display most frequent combination of start station and end station trip
        time_delay_short()
        most_common_start_end_station = df[['Start Station', 'End Station']].mode(0)
        print('Most Common Start and End Station: \n',most_common_start_end_station)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def trip_duration_stats(df):
        #Displays statistics on the total and average trip duration.
        print('\nCalculating Trip Duration for: \n City:  {}\n Month: {}\n Day:   {}'.format(city,month,day))

        time_delay_short()
        start_time = time.time()

        # TO DO: display total travel time
        Total_travel_time = df['Trip Duration'].sum(axis = 0, skipna = True)
        print('Total travel time for: \n City:  {}\n Month: {}\n Day:   {}'.format(city,month,day))
        print('is... ' , display_time(Total_travel_time))

        time_delay_short()

        # TO DO: display mean travel time
        Mean_travel_time = df['Trip Duration'].mean(axis = 0, skipna = True)
        print('Total average travel time for: \n City:  {}\n Month: {}\n Day:   {}'.format(city,month,day))
        print('is... ', display_time(Mean_travel_time))

        time_delay_short()

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def user_stats(df):
        #Displays statistics on bikeshare users.
        print('\nCalculating User Stats: \n City:  {}\n Month: {}\n Day:   {}'.format(city,month,day))

        time_delay_short()

        start_time = time.time()

        # Display counts of user type
        x = 'User Type'
        print('\nCount of User Type:\n',df[x].value_counts())

        time_delay_short()
        # Display counts of gender
        y = 'Gender'
        print('\nCount of Gender:\n',df[y].value_counts())

        # Display earliest, most recent, and most common year of birth
        z = 'Birth Year'
        currentYear = datetime.now().year
        oldest_biker = currentYear - df[z].min()
        print('\nOldest User is {} years old!'.format(oldest_biker))
        print('Wow that\'s old!')

        youngest_biker = currentYear - df[z].max()
        print('\nYoungest User is {} years old!'.format(youngest_biker))
        print('Wow that\'s young!')

        common_year = currentYear - df[z].mode()
        print('\nMost common age of users in data set is {} years old'.format(common_year))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def display_raw_data():

        # get user input whether to displays cycle through 5 rows of data
        raw_data_display = input("Would you like to see 5 records of the data? Press any key to continue displaying or type 'pass' to skip to descriptive statistics \n")
        if raw_data_display != 'pass':
            i = 5
            while raw_data_display !='pass':
                print(df.iloc[i-5:i, :])
                raw_data_display = input("Would you like to see the next 5 records of raw data? Press any key to continue displaying or type 'pass' to skip to descriptive statistics \n")
                i = i + 5

            else:
                print("....skipping ahead to descriptive stats\n")

    def drop_na_values():
        global df
        # get number of rows in dataframe
        numOfRows = df.shape[0]
        print('\nThe raw data set is {} rows long!\n'.format(numOfRows))

        time_delay_short()

        print('\nAnalyzing for number of blank fields in the raw dataset...\n')

        time_delay_long()

        nan_count = df.isnull().sum()
        print ('\nNumber of blank fields of each column in our dataset:\n', nan_count)

        time_delay_short()

        count_of_non_nan = df.count()
        print ('\nCount of number of completed fields in our data set:\n', count_of_non_nan)

        print ('\nWe will now drop the rows with blanks from the dataset so that the calculated statistics will not be skewed...\n')
        df.dropna(axis = 0, inplace = True)
        time_delay_long()

        numOfRows = df.shape[0]
        print('\nThe modified data set is now {} rows long!'.format(numOfRows))

    def time_delay_long():
    #to add time delay to slow down the bombard of text to the user (and for fun!)
        time.sleep(1)
        print('...executing task...')
        time.sleep(4)
        print('.........................Complete!\n')
        time.sleep(2)

    def time_delay_short():
    #to add time delay to slow down the bombard of text to the user (and for fun!)
        time.sleep(1)
        print('...executing task...')
        time.sleep(2)
        print('....................Complete!\n')
        time.sleep(1)

    get_filters()
    print('\nThe bike data will now be filtered by the following: \n City:  {}\n Month: {}\n Day:   {}'.format(city,month,day))

    load_data(city,month,day)

    drop_na_values()

    display_raw_data()

    continue_choice = input("Time stats will now be displayed. Press any key to continue or type 'pass' to skip to station stats\n").lower()

    if continue_choice != 'pass':
        time_stats(df)
    else:
        print("....skipping time stats\n")

    continue_choice = input("Station stats will now be displayed. Press any key to continue or type 'pass' to skip to trip duration stats\n").lower()
    if continue_choice != 'pass':
        station_stats(df)
    else:
        print("....skipping station_stats\n")

    continue_choice = input("Trip duration stats will now be displayed. Press any key to continue or type 'pass' to skip to trip user stats\n").lower()
    if continue_choice != 'pass':
        trip_duration_stats(df)
    else:
        print("....skipping trip duration stats\n")

    if city != "washington":
        continue_choice = input("User stats will now be displayed. Press any key to continue or type 'pass' to skip\n").lower()
        if continue_choice != 'pass':
            user_stats(df)
        else:
            print("....skipping user stats\n")
    else:
        print('Washington data set contains no gender or user type data therefore there are no user stats to display for this city! T_T )')

    #restart code
    restart = input("Do you wish to try again? y/n\n").lower()
    if restart == 'y':
        main()
    else:
        exit()
main()
