# Sensus
Twitter Sentiment Analysis with Geographic Visualization


Description
------------
Sensus uses geo-coded tweets to map sentiment data on a friendly UI.
Tweets are gathered from multiple regions using the [Twitter Developer API](https://developer.twitter.com/en/docs/tweets/search/overview), analyzed using [Scikit Learn](https://scikit-learn.org/stable/) alongside various natural language processing techniques, and then visualized in the format of a simple web application with the help of [Leaflet](https://leafletjs.com/).
.


Usage
------------
* Add your Twitter Developer API credentials to api_keys.py
  - You are subject to rate limiting depending on the tier of your account
* run  `python train_model.py`
  - This step only needs to be done once. 
  - It trains the model, outputs model accuracy, and populates the cached_model files.
  - From here on out, Sensus will use these cached models 
* run  `python sensus.py`  
  - This will start running a Flask server at localhost:80


Dependencies
------------
* scikit-learn
* tweepy
* Flask
* pandas
