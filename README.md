             Youtube Data Harvesting and Warehousing

Brief:
1.	Importing Necessary Libraries: The script starts by importing essential libraries for tasks such as accessing the YouTube API, managing databases, and creating a user interface.
2.	Functions for Interacting with YouTube API: It defines functions to interact with the YouTube API, allowing it to fetch data like channel information, video IDs, details, comments, and playlist details.
3.	Uploading Data to MongoDB: The script connects to a MongoDB database and uploads various data (channel, playlist, video, and comment information) into collections for easy retrieval and manipulation.
4.	Uploading Data to PostgreSQL: It establishes a connection to a PostgreSQL database, creates tables for storing different types of data, and populates these tables with information fetched from MongoDB.
5.	Streamlit Interface: The script defines a Streamlit interface providing functionalities for users to interact with the data. Users can browse through channels, watch videos, read comments, and perform tasks like collecting new data, migrating it to SQL, and visualizing it.


Part 1: Importing Necessary Libraries

The script begins by importing libraries that are essential for different tasks it will perform:
 
![image](https://github.com/bhaskarachalla/Youtube-Data-Harvesting/assets/157194398/272125b9-f5c4-4626-b4f2-0b621a799d7f)

These libraries provide functions and tools necessary for fetching data from the YouTube API, managing databases, and creating a user interface.

Part 2: Functions for Interacting with YouTube API

The script defines several functions to interact with the YouTube API:

 ![image](https://github.com/bhaskarachalla/Youtube-Data-Harvesting/assets/157194398/6ae88e84-258d-4e77-9f24-187ae638e62a)

These functions encapsulate API requests to fetch various data such as channel information, video IDs, video details, comments, and playlist details.

Part 3: Uploading Data to MongoDB

The script connects to a MongoDB database and uploads channel, playlist, video, and comment information:

![image](https://github.com/bhaskarachalla/Youtube-Data-Harvesting/assets/157194398/5a193152-3b7d-4274-81e3-f888d24dddf2)

 It organizes data into collections within the MongoDB database for easy retrieval and manipulation.

Part 4: Uploading Data to PostgreSQL

The script establishes a connection to a PostgreSQL database and creates tables for storing channel, playlist, video, and comment information:

![image](https://github.com/bhaskarachalla/Youtube-Data-Harvesting/assets/157194398/60fe0bb2-32be-4df6-8304-dd20a9527c1d)

 
It then populates these tables with data fetched from MongoDB.


Part 5: Streamlit Interface

The script defines a Streamlit interface with various functionalities:

![image](https://github.com/bhaskarachalla/Youtube-Data-Harvesting/assets/157194398/f2a974e5-8328-4773-a679-3fa4aeb61676)

 
This interface allows users to interact with the data, collect new data, migrate it to SQL, and visualize it.

Example:
1.Imagine you have a favourite YouTube channel. This script acts like a personal assistant that can browse through the channel, watch videos, read comments, 
and remember everything. You can ask it questions like "Show me the top 10 most viewed videos" or "How many likes does each video have?" 
It fetches this data for you from YouTube, organizes it neatly into databases, and presents it in a user-friendly way through a web interface.

2.Real-time Example: Let's say you're running a marketing agency, and you want to analyze the performance of various YouTube channels related to your clients' industries. You can use this script to gather data on channel demographics, video engagement, and viewer interactions. With the collected data, you can generate insights such as which channels have the most active subscribers, which videos attract the most views, and what types of content receive the highest engagement. These insights can inform your marketing strategies, helping you optimize content creation, identify potential collaboration opportunities, and target specific audience segments more effectively. Additionally, the Streamlit interface allows you to interactively explore and visualize the data, making it easy to communicate your findings to clients or team members.
