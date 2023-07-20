import pandas as pd
import numpy as np
import time


CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'w': 'washington.csv' }


def get_filters():
    """
   Asks user to choose a city, month, and day to analyze.

    Returns:
    (str) city - name of the city that the user would choose
    (str) month - name of specific month to filter by , or "all" word for no filter 
    (str) day - name of specific day , or "all" word for apply no day filter
    """
    
    while True:
            city = input("\nPlease select the city by typing:\n\nch for chicago\nw for washington\nny for New york city : ").lower()
            if city in CITY_DATA.keys():
                break
            else:
                print('\nWrong input!!!, please try again by typing day name or all\n')


    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']
    while True:
        month = input("\nWant a data for a specific month! please type the month,, 'if not type all'..\n(jan-feb-mar-apr-may-jun-all) : ").lower()
        if month in months:
            break
        else:
            print('\nWrong input!!!, please try again by typing month name or all\n')

    days = ['sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'all']
    while True:
        day = input("\nWant a data for a specific day! please type the day,, 'if not type all'..\n(sat-sun-mon-tue-wed-thu-fri-all) : ").lower()
        if day in days:
              break
        else:
            print('\nWrong input!!!, please try again\n')


    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specific city and filter the data by month and day if applicable.

    Args:
    (str) city - name of the city that the user would choo
    (str) month - name of specific month to filter by , or "all" word for no filter 
    (str) day - name of specific day , or "all" word for apply no day filter
    Returns:
    (df) Pandas DataFrame containing city data with or with out filter
    """
    
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day of week'] = df['Start Time'].dt.day_name()

    if month != 'all':
         months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']
         month = months.index(month) + 1
         df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day of week'].str.startswith(day.title())]



    return df

def time_stats(df):
    """this function gets the data fram from get_filters function and apply statistics on the most frequent times of travel to return most common day, month and hour."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #caclculate the most common month and its count
    common_month = df['month'].mode()[0]
    common_month_count = len([month for month in df['month'] if month == common_month])
    #calculate the most common day of week ant its count
    common_day = df['day of week'].mode()[0]
    common_day_count = len([day for day in df['day of week'] if day == common_day])
    #calculate the most common start hour and its count
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    common_hour_count = len([hour for hour in df['hour'] if hour == common_hour])

    print('Most common month: {}, count: {}\nMost common day: {}, count: {}\nMost common hour: {}, count: {}\n'.format(common_month, common_month_count, common_day, common_day_count, common_hour, common_hour_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """this function gets the data fram from get_filters function and apply statistics on stations to return the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #calculate most commonly used start station and its count
    common_start_station = df['Start Station'].mode()[0]
    common_start_station_count = len([ss for ss in df['Start Station'] if ss == common_start_station])
    #calculate most commonly used end station and its count
    common_end_station = df['End Station'].mode()[0]
    common_end_station_count = len([es for es in df['End Station'] if es == common_end_station])
    #calculate most frequent combination of start station and end station trip and its count
    df['Trip'] = "from " + df['Start Station'] + " to " + df['End Station']

    common_trip = df['Trip'].mode()[0]
    common_trip_count = len([trip for trip in df['Trip'] if trip == common_trip])

    print('Most common start station: {}, count: {}\nMost common end station: {}, count: {}\nMost common trip: {}, count: {}\n'.format(common_start_station, common_start_station_count, common_end_station, common_end_station_count, common_trip, common_trip_count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 
    
def trip_duration_stats(df):
    """that function gets the data fram from get_filters function and apply statisticss on trip duration  to return the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #calculate total travel time
    total_travel_time = df.loc[:,['Trip Duration']].sum()[0]

    #calculate mean travel time
    average_travel_time = df.loc[:,['Trip Duration']].mean()[0]

    print('Total travel time : {}\nAverage tavel time : {}\n'.format(total_travel_time, average_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """that function gets the data fram from get_filters function and apply statistics on bikeshare users to return the count of user types, gender and most common, earliest, recent year."""
    print('\nCalculating User Stats...')
    start_time = time.time()
    
    #calculate counts of user types
    user_types =  df['User Type'].value_counts().to_frame()
    
    #calculate counts of gender and most common and earliest and recent year
    if 'Gender' and 'Birth Year' not in df.columns:
        print('\n','User types : {}'.format(user_types), '\n\nGender and birth year data is not available in washington..\n')
    else:
        gender_types = df['Gender'].value_counts().to_frame()
        most_recent_y = int(df.loc[:,['Birth Year']].max()[0])
        most_recent_y_count = len([rs for rs in df['Birth Year'] if rs == most_recent_y])
        most_common_y = int(df['Birth Year'].mode()[0])
        most_common_y_count = len([cy for cy in df['Birth Year'] if cy == most_common_y])
        earliest_y = int(df.loc[:,['Birth Year']].min()[0])
        earliest_y_count = len([ey for ey in df['Birth Year'] if ey == earliest_y])
        print('\n\nUser types : {}\n\nGender types : {}\n\nMost common year of birth : {}, count: {}\nMost recent year of birth : {}, count: {}\nEarliest year of birth : {}, count: {}\n'.format(user_types, gender_types, most_common_y, most_common_y_count, most_recent_y, most_recent_y_count, earliest_y, earliest_y_count))
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(city):
    """This fuction gets the city name from the get_filters fuction  and returns the raw data of that city based on users decision.
    """
    df = pd.read_csv(CITY_DATA[city])

    loc = 0

    while True:
        in_put = input('Want to see the raw data? answer with yes or no \n').lower()
        if in_put == 'yes':
            print(df.iloc[loc:loc+5])
            loc += 5
        elif in_put == 'no':
            break
        else:
             print('\nWrong input!!!, please try again by answering with yes or no\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
