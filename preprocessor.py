import re
import pandas as pd
def preprocess(data):
    pattern = "(\d{1,2}\/\d{1,2}\/\d{2,4}),\s(\d{1,2}:\d{2}\s?[ap]m)\s-\s"


    #extracting then structuring data list
    messages = re.split(pattern, data)[1:]
    messages = [msg.replace('\u202f', ' ') for msg in messages]
    structured_list = [
        {'date': messages[i], 'time': messages[i + 1], 'user_message': messages[i + 2]}
        for i in range(0, len(messages), 3)
    ]
    df = pd.DataFrame(structured_list)
    # removing errored msgs
    df = df[~df['user_message'].str.contains('\x00', case=False, na=False)].reset_index(drop=True)

    #extracting user and msg from user_msg
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['msg'] = messages
    #dropping the raw msg column
    df.drop(columns=['user_message'], inplace=True)

    #now extracting more
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']= df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date

    # extract from time as its in string format
    df['hour'] = df['time'].str.split(':').str[0].str.split(' ').str[0]
    df['minute'] = df['time'].str.split(':').str[1].str.split(' ').str[0]
    df['meridiem'] = df['time'].str.split(' ').str[1]

    period = []

    for hour in df[['day_name', 'hour']]['hour']:
        hour = int(hour)  # ensure hour is an integer
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour:02d}-{(hour + 1):02d}")

    df['period'] = period

    return df

