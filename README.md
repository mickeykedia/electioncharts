# Election Charts

This is a repo for an interactive web interface for showing election data live. This was deployed for the Indian General Elections in 2014 on (www.electioncharts.com). This website is no longer up, but it shouldn't take too long to redeploy it again. 

The facebook page showing screenshots etc from the original app is at [https://www.facebook.com/electioncharts](https://www.facebook.com/electioncharts). 

A live demo of the **Bird Swing Graph** can be found at [here](http://bl.ocks.org/mickeykedia/4d247c4741cdbccef3a527f5201275f4)

# Basic structure

As was originally deployed, this app was a flask app deployed on Google App Engine for Automatic scaling. We were using the Google App Engine's MySQL db for the underlying database of the APP. 

On the front end this was an Angular JS, D3js, Bootstrap based application. 

# Data

Election data for General Elections 2014 (India) and 2009 is available in `data` folder. This is very clean data that has been cleaned very meticulously by scraping from multiple sources and making sure that there is consistency in name of constitutencies, parties, candidate names etc across the two years and amongst each other. 

Note: Telanga has not been included in the data because the state came into existence only after the general elections. Though it should be easy to recreate telangana because the Parliamentary Constituencies haven't been changed and you only need to reassign the relevant constituencies from Andhra Pradesh to Telangana. 

# To do 

- Since the tables had been written for a live update framework where new data is pushed into the tables every minute during the counting of votes, the queries are not optimized for use in a static setting (when the data isnt' changing)
- Redeploy the app on Google App engine
- Needs thorough testing for scalability








