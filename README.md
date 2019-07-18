# Sensus
Twitter Sentiment Analysis with Geographic Visualization


Description
------------
Sensus uses Twitter content from geo-coded tweets to map sentiment data on a friendly UI. 
Tweets are gathered from multiple regions, analyzed using various natural language processing techniques, and then 
visualized in the format of a web application with the help of [Leaflet](https://leafletjs.com/).
.


Usage
------------
* Add your Twitter Developper API credentials to api_keys.py
* run  `python sensus.py`  
  - This will start running a Flask server at localhost:80
  

Dependencies
------------
* scikit-learn
* tweepy
* python Flask
* pandas
