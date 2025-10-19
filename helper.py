from collections import Counter
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud,STOPWORDS
import re,string
import emoji



def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    #col1
    num_msgs = df.shape[0]

    #col2
    words = []
    for msg in df['msg']:
        words.extend(msg.split())
    num_words = len(words)

    #col3
    num_media = df[df['msg']== '<Media omitted>\n'].shape[0]

    #col4
    ext = URLExtract()
    links = []
    for msgs in df['msg']:
        links.extend(ext.find_urls(msgs))

    return num_msgs, num_words , num_media, len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    df= round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percentage'})
    return x, df

def create_wordcloud(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['msg'] != '<Media omitted>\n']
    temp = temp[temp['msg'] != 'media']
    temp = temp[temp['msg'] != 'omitted']
    temp = temp[temp['msg'] != 'This message was deleted\n']

    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()

    extra_stopwords = ['media', 'omitted', 'file', 'attached', 'img', 'webp', 'edited', 'message', 'hh', 'aa', 'h','hai']

    # Combine with stopwords from file
    stop_words = set(stop_words) | set(extra_stopwords)

    refind_word = []
    for msgs in temp['msg']:
        for word in msgs.lower().split():
            # Remove punctuation from word
            word_clean = word.strip(string.punctuation)
            if word_clean and word_clean not in stop_words:
                refind_word.append(word_clean)

    text = " ".join(refind_word)

    # 🧹 Clean text: remove unwanted tokens
    text = re.sub(r'STK[\s_-]*WA[\s_-]*\w*', '', text,
                  flags=re.IGNORECASE)  # removes STKWA, STK WA0001, STK-WA0001, etc.
    text = re.sub(r'IMG[\s_-]*\w*', '', text, flags=re.IGNORECASE)  # removes IMG1234, IMG-20231014, etc.
    text = re.sub(r'VID[\s_-]*\w*', '', text, flags=re.IGNORECASE)  # removes VID1234, etc.
    text = re.sub(r'\bwebp\b|\bjpg\b|\bpng\b|\bmp4\b', '', text, flags=re.IGNORECASE)  # remove extensions
    text = re.sub(r'<Media omitted>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'http\S+|www\S+', '', text)  # remove links
    text = re.sub(r'\d+', '', text)  # remove standalone numbers
    text = re.sub(r'[^A-Za-z\s]+', '', text)  # remove punctuation, emojis, and symbols
    print(type(text))
    # 🧩 Custom stopwords
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update([
        'media', 'omitted', 'message', 'deleted',
        'file', 'attached', 'img', 'webp', 'stk', 'wa', 'photo', 'video','stkwa'
    ])
    wc = WordCloud(width=500, height=500, min_font_size=10 ,stopwords=custom_stopwords, background_color='white')
    df_wc = wc.generate(text)

    most_common_words_df = pd.DataFrame(Counter(refind_word).most_common(20))

    return df_wc,most_common_words_df

# def most_common_words(df):
#     x = df['user'].value_counts().head()

def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for msgs in df['msg']:
        emojis.extend([c for c in msgs if emoji.is_emoji(c)])

    emoji_df= pd.DataFrame(Counter(emojis).most_common(10))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['msg'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_timeline_df = df.groupby('only_date').count()['msg'].reset_index()

    return daily_timeline_df

def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heapmap(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='msg', aggfunc='count').fillna(0)

    return user_heatmap