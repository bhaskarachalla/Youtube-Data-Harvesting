import googleapiclient.discovery
import pymongo
import psycopg2
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build

def Api_connect():
    Api_Id= "AIzaSyBKnvQEZmQyt-T8VizFlUdpAPe80p5LQgc"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(api_service_name, api_version,developerKey= Api_Id)
    
    return youtube
youtube=Api_connect()

request = youtube.channels().list(
part = "snippet,contentDetails,statistics",
id = "UCZ0hNUqXDl0YWh3ulUZy1jQ" #VR Raja
)
response = request.execute()

def channel_info(c_id):
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=c_id
    )
    response = request.execute()
   
    data = {
          'Channel_name':response['items'][0]['snippet']['title'],
          'Channel_id':response['items'][0]['id'],
          'Description':response['items'][0]['snippet']['description'],
          'Published_Date': response['items'][0]['snippet']['publishedAt'],
          'Playlist_id': response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
          'Subscribers': response['items'][0]['statistics']['subscriberCount'],
          'Views':  response['items'][0]['statistics']['viewCount'],
          'Total_Videos': response['items'][0]['statistics']['videoCount']
    }

    return data

def video_id(c_id):
    video_ids=[]
    response=youtube.channels().list(id = c_id,
                                    part='contentDetails').execute()
    Playlist_Id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
        part="snippet",
        playlistId = Playlist_Id,
        maxResults=5,# imported from google cilent each and every page gives 10 results and if the last page doesn't contain 10 then the the number which are there are printed
        pageToken = next_page_token) #maxresults is used to return the maximum number of items that should be returned in the result
        response1 = request.execute() #defining a new variable 


        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = response1.get('nextPageToken') #get function prevents obtaining an error while calling at the end of the pages
        
        if next_page_token is None: #to break the while loop
            break
    return video_ids

def video_Info(video_ids):
    video_data=[]
    for video_id in video_ids:
        request = youtube.videos().list(
            part = "snippet,contentDetails,statistics",
            id = video_id
        )
        response = request.execute()
            
        for item in response['items']:
            data = dict(Channel_Name = item['snippet']['channelTitle'],
                        Channel_Id = item['snippet']['channelId'],
                        Video_Id = item['id'],
                        Title = item['snippet']['title'],
                        Tags = item['snippet'].get('tags'), #since we used get function error will give us a none value as return
                        Thumbnail = item['snippet']['thumbnails']['default']['url'],
                        Description = item['snippet'].get('description'), #since we used get function error will give us a none value as return
                        Published_Date = item['snippet']['publishedAt'],
                        Duration = item['contentDetails']['duration'],
                        Views = item['statistics'].get('viewCount'), #since we used get function error will give us a none value as return
                        Likes = item['statistics'].get('likeCount'),
                        Comments = item['statistics'].get('commentCount'), #since we used get function error will give us a none value as return
                        Favorite_Count = item['statistics']['favoriteCount'],
                        Definition = item['contentDetails']['definition'],
                        caption_status = item['contentDetails']['caption'],
                        )  
            video_data.append(data)
    return video_data

def Comment_Info(video_id):
    Comment_data = []
    try:
        for video_id in video_id:
            request = youtube.commentThreads().list(
                part = "snippet",
                videoId = video_id,
                maxResults = 5
            )
            response = request.execute()
            
            
            for item in response['items']:
                data = dict(Comment_Id = item['snippet']['topLevelComment']['id'],
                            Video_Id = item['snippet']['topLevelComment']['snippet']['videoId'],
                            Comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay'],
                            Comment_Author = item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            Comment_Published = item['snippet']['topLevelComment']['snippet']['publishedAt'],
                            
                            )
                Comment_data.append(data)
    except:
        pass
    return Comment_data

def Playllist_Details(c_id):
    next_page_token = None
    Complete_Data = []
    while True:
        request = youtube.playlists().list(
            part = 'snippet, contentDetails',
            channelId = c_id,
            maxResults = 50,
            pageToken = next_page_token
        )
        response = request.execute()

        for item in response['items']:
                data = dict(Playlist_id = item['id'],
                            Playlist_title = item['snippet']['title'],
                            Channel_Id = item['snippet']['channelId'],
                            Channel_Name = item['snippet']['channelTitle'],
                            Playlist_Date = item['snippet']['publishedAt'],
                            Video_Count = item['contentDetails']['itemCount'],
                            )
                Complete_Data.append(data)
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break
    return Complete_Data

#mongodb uploading
client = pymongo.MongoClient('mongodb+srv://bhaskarachalla054:9ybuE5KLUOFB065T@cluster0.xrekhya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['Youtube_Data']

def channel_details(c_id):
    ch_details = channel_info(c_id)
    pl_details = Playllist_Details(c_id)
    vi_id = video_id(c_id)
    vi_details = video_Info(vi_id)
    com_details = Comment_Info(vi_id)
    
    
    collection2 = db['channel_details'] #connection to databse by this line of code
    collection2.insert_one({'channel_information':ch_details,
                            'playlist_information':pl_details,
                            'video_information':vi_details,
                            'comment_information':com_details}) #converting json files into mongodb we use a flower brackets inside paranthesis
    return 'Upload Successful'

def channels_table():

    mydb = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        password = 'Space-time123',
                        database = 'YT_Data',
                        port = '5432')
    cursor = mydb.cursor()


    drop_query = '''drop table if exists channels'''
    cursor.execute(drop_query)
    mydb.commit()

    try:
        create_query = '''create table if not exists channels(Channel_name varchar(100),
                                                            Channel_id varchar(80) primary key,
                                                            Description text,
                                                            Published_Date timestamp,
                                                            Playlist_id varchar(80),
                                                            Subscribers bigint,
                                                            Views bigint,
                                                            Total_Videos int)'''
        cursor.execute(create_query)
        mydb.commit()
        
    except:
        print('Channel Tables already created')
        

    ch_list = []
    db = client['Youtube_Data'] #science client name in db is this and don't be confused with sql name
    collection2 = db['channel_details']
    #for retriving all the channels data from mongodb an empty curles are used and if any selected channels are required we can mention in the curles
    #the second curles are for getting required information from the selected channel
    for ch_data in collection2.find({},{'_id': 0,'channel_information':1}):
        ch_list.append(ch_data["channel_information"])
    df = pd.DataFrame(ch_list)


    for index,row in df.iterrows():
        insert_query = '''insert into channels(Channel_name,
                                            Channel_id,
                                            Description,
                                            Published_Date,
                                            Playlist_id,
                                            Subscribers,
                                            Views,
                                            Total_Videos)
                                            
                                            values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        
        values = (row['Channel_name'],
                row['Channel_id'],
                row['Description'],
                row['Published_Date'],
                row['Playlist_id'],
                row['Subscribers'],
                row['Views'],
                row['Total_Videos'],
                )
                
        try:
            cursor.execute(insert_query,values)
            mydb.commit()
        except:
            print('channel is already filled')

def playlist_table():

    mydb = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        password = 'Space-time123',
                        database = 'YT_Data',
                        port = '5432')
    cursor = mydb.cursor()


    drop_query = '''drop table if exists playlists'''
    cursor.execute(drop_query)
    mydb.commit()


    create_query = '''create table if not exists playlists(Playlist_id varchar(100) primary key,
                                                        Playlist_title varchar(100),
                                                        Channel_Id varchar(100),
                                                        Channel_Name varchar(100),
                                                        Playlist_Date timestamp,
                                                        Video_Count int)'''
    cursor.execute(create_query)
    mydb.commit()
    
    
    pl_list = []
    db = client['Youtube_Data']
    collection2 = db['channel_details']
    #for retriving all the channels data from mongodb an empty curles are used and if any selected channels are required we can mention in the curles
    #the second curles are for getting required information from the selected channel
    for pl_data in collection2.find({},{'_id': 0,'playlist_information':1}):
        for i in range(len(pl_data['playlist_information'])):
            pl_list.append(pl_data['playlist_information'][i])
    df1 = pd.DataFrame(pl_list)
    
    
    mydb = psycopg2.connect(host = 'localhost',
                    user = 'postgres',
                    password = 'Space-time123',
                    database = 'YT_Data',
                    port = '5432')
    cursor = mydb.cursor()

    for index,row in df1.iterrows():
            insert_query = '''insert into playlists(Playlist_id,
                                                Playlist_title,
                                                Channel_Id,
                                                Channel_Name,
                                                Playlist_Date,
                                                Video_Count)
                                            
                                            values(%s,%s,%s,%s,%s,%s)'''
    
            values = (row['Playlist_id'],
                  row['Playlist_title'],
                  row['Channel_Id'],
                  row['Channel_Name'],
                  row['Playlist_Date'],
                  row['Video_Count']
                  )
            cursor.execute(insert_query,values)
            mydb.commit()

def videos_table():

    mydb = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        password = 'Space-time123',
                        database = 'YT_Data',
                        port = '5432')
    cursor = mydb.cursor()


    drop_query = '''drop table if exists videos'''
    cursor.execute(drop_query)
    mydb.commit()


    create_query = '''create table if not exists videos(Channel_Name varchar(100),
                                                        Channel_Id varchar(100),
                                                        Video_Id varchar(20) primary key,
                                                        Title varchar(200),
                                                        Tags text, 
                                                        Thumbnail varchar(200),
                                                        Description text, 
                                                        Published_Date timestamp,
                                                        Duration interval,
                                                        Views bigint, 
                                                        Likes bigint,
                                                        Comments int, 
                                                        Favorite_Count int,
                                                        Definition varchar(10),
                                                        Caption_status varchar(90))'''
    cursor.execute(create_query)
    mydb.commit()

    vd_list = []
    db = client['Youtube_Data']
    collection2 = db['channel_details']
    for vd_data in collection2.find({},{'_id': 0,'video_information':1}):
        for i in range(len(vd_data['video_information'])):
            vd_list.append(vd_data['video_information'][i])
    df2 = pd.DataFrame(vd_list)


    for index,row in df2.iterrows():
        insert_query = '''insert into videos(Channel_Name,
                                            Channel_Id,
                                            Video_Id,
                                            Title,
                                            Tags,
                                            Thumbnail,
                                            Description,
                                            Published_Date,
                                            Duration,
                                            Views,
                                            Likes,
                                            Comments,
                                            Favorite_Count,
                                            Definition,
                                            Caption_status
                                            )
                                        
                                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        values = (row['Channel_Name'],
                    row['Channel_Id'],
                    row['Video_Id'],
                    row['Title'],
                    row['Tags'],
                    row['Thumbnail'],
                    row['Description'],
                    row['Published_Date'],
                    row['Duration'],
                    row['Views'],
                    row['Likes'],
                    row['Comments'],
                    row['Favorite_Count'],
                    row['Definition'],
                    row['caption_status'])
        
        
        cursor.execute(insert_query,values)
        mydb.commit()

def comments_table():

    mydb = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        password = 'Space-time123',
                        database = 'YT_Data',
                        port = '5432')
    cursor = mydb.cursor()


    drop_query = '''drop table if exists comments'''
    cursor.execute(drop_query)
    mydb.commit()


    create_query = '''create table if not exists comments(Comment_Id varchar(100) primary key,
                                                        Video_Id varchar(100),
                                                        Comment_text text,
                                                        Comment_Author varchar(200),
                                                        Comment_Published timestamp)'''
    cursor.execute(create_query)
    mydb.commit()

    com_list = []
    db = client['Youtube_Data']
    collection2 = db['channel_details']
    for com_data in collection2.find({},{'_id': 0,'comment_information':1}):
        for i in range(len(com_data['comment_information'])):
            com_list.append(com_data['comment_information'][i])
    df3 = pd.DataFrame(com_list)


    for index,row in df3.iterrows():
            insert_query = '''insert into comments(Comment_Id,
                                                Video_Id,
                                                Comment_text,
                                                Comment_Author,
                                                Comment_Published)
                                            
                                            values(%s,%s,%s,%s,%s)'''

            values = (row['Comment_Id'],
                    row['Video_Id'],
                    row['Comment_text'],
                    row['Comment_Author'],
                    row['Comment_Published']
                    )
            cursor.execute(insert_query,values)
            mydb.commit()

def All_tables():
    channels_table()
    playlist_table()
    videos_table()
    comments_table()
    
    return 'Tables Created Successfully'

def show_Channels():

    ch_list = []
    db = client['Youtube_Data'] #science client name in db is this and don't be confused with sql name
    collection2 = db['channel_details']
    #for retriving all the channels data from mongodb an empty curles are used and if any selected channels are required we can mention in the curles
    #the second curles are for getting required information from the selected channel
    for ch_data in collection2.find({},{'_id': 0,'channel_information':1}):
        ch_list.append(ch_data["channel_information"])
    df = st.dataframe(ch_list)  
    
    return df

def show_Playlists():
    pl_list = []
    db = client['Youtube_Data']
    collection2 = db['channel_details']
    #for retriving all the channels data from mongodb an empty curles are used and if any selected channels are required we can mention in the curles
    #the second curles are for getting required information from the selected channel
    for pl_data in collection2.find({},{'_id': 0,'playlist_information':1}):
        for i in range(len(pl_data['playlist_information'])):
            pl_list.append(pl_data['playlist_information'][i])
    df1 = st.dataframe(pl_list)
    
    return df1

def show_Videos():
    vd_list = []
    db = client['Youtube_Data']
    collection2 = db['channel_details']
    for vd_data in collection2.find({},{'_id': 0,'video_information':1}):
        for i in range(len(vd_data['video_information'])):
            vd_list.append(vd_data['video_information'][i])
    df2 = st.dataframe(vd_list)
    
    return df2

def show_Comments():
    com_list = []
    db = client['Youtube_Data']
    collection2 = db['channel_details']
    for com_data in collection2.find({},{'_id': 0,'comment_information':1}):
        for i in range(len(com_data['comment_information'])):
            com_list.append(com_data['comment_information'][i])
    df3 = st.dataframe(com_list)
    
    return df3

with st.sidebar:
    st.title(':red[YouTube Data Harvesting and Warehousing]')
    st.header('Project Details')
    st.caption('Python Scripting')
    st.caption('Data Retriving')
    st.caption('MongoDB Connection')
    st.caption('Data Management using MongoDB and SQL')
    
channel_id = st.text_input('Please enter Channel ID :')

if st.button('Collect and Store Data'):
    ch_ids = []
    db = client['Youtube_Data']
    collection2 = db['channel_details']
    for ch_data in collection2.find({},{'_id':0,'channel_information':1}):
        ch_ids.append((ch_data['channel_information']['Channel_id']))
    
    if channel_id in ch_ids:
        st.success("Channel details exists")
    
    else:
        insert = channel_details(channel_id)
        st.success(insert)

if st.button('Migrate to SQL'):
    Table = All_tables()
    st.success(Table)
    
show_table = st.radio('Select the table for view',('Channels','Playlists','Videos','Comments'))

if show_table == 'Channels':
    show_Channels()
elif show_table == 'Playlists':
    show_Playlists()
elif show_table == 'Videos':
    show_Videos()
elif show_table == 'Comments':
    show_Comments()   
mydb = psycopg2.connect(host = 'localhost',
                    user = 'postgres',
                    password = 'Space-time123',
                    database = 'YT_Data',
                    port = '5432')
cursor = mydb.cursor()

question = st.selectbox('Select your question',('1.All the videos and the channel name',
                                                '2.Channels with most number of videos',
                                                '3.Top 10 viewed videos',
                                                '4.Comments in each video',
                                                '5.Videos with highest likes',
                                                '6.Likes of all videos',
                                                '7.Views of each channel',
                                                '8.Videos published in 2022',
                                                '9.Average duration of all videos in each channel',
                                                '10.Videos with highest number of comments'))

if question == '1.All the videos and the channel name':
    query1 = '''select title as videos, channel_name as channelname from videos'''
    cursor.execute(query1)
    mydb.commit()
    t1 = cursor.fetchall()
    df = pd.DataFrame(t1,columns = ['video title','channel name'])
    st.write(df)

elif question == '2.Channels with most number of videos':
    query2 = '''select channel_name as channelname,total_videos as no_videos from channels 
                order by total_videos desc'''
    cursor.execute(query2)
    mydb.commit()
    t2 = cursor.fetchall()
    df1 = pd.DataFrame(t2,columns = ['channel name','No of Videos'])
    st.write(df1)

elif question == '3.Top 10 viewed videos':
    query3 = '''select views as views,channel_name as channelname,title as videotitle from videos 
                where views is not null order by views desc limit 10'''
    cursor.execute(query3)
    mydb.commit()
    t3 = cursor.fetchall()
    df2 = pd.DataFrame(t3,columns = ['views','channel_name','videotitle'])
    st.write(df2)

elif question == '4.Comments in each video':
    query4 = '''select comments as no_comments,title as videotitle from videos where comments is not null'''
    cursor.execute(query4)
    mydb.commit()
    t4 = cursor.fetchall()
    df3 = pd.DataFrame(t4,columns = ['no of comments','videotitle'])
    st.write(df3)

elif question == '5.Videos with highest likes':
    query5 = '''select title as videotitle,channel_name as channelname,likes as likecount
                from videos where likes is not null order by likes desc'''
    cursor.execute(query5)
    mydb.commit()
    t5 = cursor.fetchall()
    df4 = pd.DataFrame(t5,columns = ['videotitle','channelname','likecount'])
    st.write(df4)

elif question == '6.Likes of all videos':
    query6 = '''select likes as likecount,title as videotitle from videos'''
    cursor.execute(query6)
    mydb.commit()
    t6 = cursor.fetchall()
    df5 = pd.DataFrame(t6,columns = ['likecount','videotitle'])
    st.write(df5)

elif question == '7.Views of each channel':
    query7 = '''select channel_name as channelname,views as totalviews from channels'''
    cursor.execute(query7)
    mydb.commit()
    t7 = cursor.fetchall()
    df6 = pd.DataFrame(t7,columns = ['channelname','totalviews'])
    st.write(df6)
    
elif question == '8.Videos published in 2022':
    query8 = '''select title as video_title,published_date as videorelease,
                channel_name as channelname from videos where extract (year from published_date) =2022'''
    cursor.execute(query8)
    mydb.commit()
    t8 = cursor.fetchall()
    df7 = pd.DataFrame(t8,columns = ['videotitle','published_date','channelname'])
    st.write(df7)

elif question == '9.Average duration of all videos in each channel':
    query9 = '''select channel_name as channelname,
                AVG(duration) as averageduration from videos group by channel_name'''
    cursor.execute(query9)
    mydb.commit()
    t9 = cursor.fetchall()
    df8 = pd.DataFrame(t9,columns = ['channelname','averageduration'])
    
    T9 = []
    for index,row in df8.iterrows():
        channel_title = row['channelname']
        average_duration = row['averageduration']
        average_duration_str = str(average_duration)
        T9.append(dict(channeltitle = channel_title,avgduration = average_duration_str))
    df1 = pd.DataFrame(T9)
    st.write(df8)

elif question == '10.Videos with highest number of comments':
    query10 = '''select title as videotitle,channel_name as channelname,comments as 
                comments from videos where comments is not null order by comments desc '''
    cursor.execute(query10)
    mydb.commit()
    t10 = cursor.fetchall()
    df9 = pd.DataFrame(t10,columns = ['videotitle','channelname','comments'])
    st.write(df9)            
    
                                #Enjoy_Coding