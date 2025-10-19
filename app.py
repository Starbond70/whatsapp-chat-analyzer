import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Analyze"):
        num_msgs, num_words, num_media_shared, num_link_shared = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_msgs)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Number of Media Shared")
            st.title(num_media_shared)
        with col4:
            st.header("Number of Links Shared")
            st.title(num_link_shared)

        #timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['msg'])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        #daily_timeline
        st.title("Daily Timeline")
        daily_timeline_df = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline_df['only_date'],daily_timeline_df['msg'],color='black')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        #activity map
        st.title("Active Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Active Day")
            active_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.barh(active_day.index,active_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Active Month")
            active_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(active_month.index, active_month.values, color = 'red')
            st.pyplot(fig)

        #Activity HeatMap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heapmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap,cmap='Oranges')
        st.pyplot(fig)

        #most active members
        if selected_user == "Overall":
            st.title("Most Active Users")
            x, new_df= helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1,col2= st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color="green")
                plt.xticks(rotation=90)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        # Word cloud
        st.title("Word Cloud")
        df_wc , most_common_words_df = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        fig, ax = plt.subplots()
        ax.barh(most_common_words_df[0],most_common_words_df[1])
        # st.dataframe(most_common_words_df)
        st.pyplot(fig)

        #emoji analysis
        st.title("most common emojis")
        emoji_df = helper.emoji_helper(selected_user,df)
        st.dataframe(emoji_df)
