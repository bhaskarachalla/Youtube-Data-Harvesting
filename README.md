             Youtube Data Harvesting and Warehouseing

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
Imagine you have a favourite YouTube channel. This script acts like a personal assistant that can browse through the channel, watch videos, read comments, 
and remember everything. You can ask it questions like "Show me the top 10 most viewed videos" or "How many likes does each video have?" 
It fetches this data for you from YouTube, organizes it neatly into databases, and presents it in a user-friendly way through a web interface.
