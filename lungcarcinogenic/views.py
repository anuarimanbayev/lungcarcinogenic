from flask import Flask, render_template, request, redirect, url_for
from insightdemo import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from pandas import DataFrame, to_datetime, Series
import psycopg2
import requests
import json
import os
import googlemaps
# from a_Model import ModelIt
# import time
# import datetime as dt
# from datetime import datetime,timedelta
# import bokeh
# from bokeh.plotting import figure, output_file, show
# from bokeh.embed import components
# from bokeh.resources import INLINE
# from bokeh.charts import Histogram, Bar
# from bokeh.charts import defaults, vplot, hplot, show, output_file
# from math import pi
# import folium


## Import from pickle the custom Database, processed lcmRadonData
lcmRadonData = pd.read_pickle("lcmRadonData")

## DATABASE LINKAGES Postgresql
user = 'anuariman7' #add your username here (same as previous postgreSQL)
pswd = 'naiman7argyn'                    
host = 'localhost'
dbname = 'lungenvfac_db'
db = create_engine('postgresql://%s:%s@localhost/%s'%(user,pswd,dbname))
## separate postgresql databases for each main feature: Lung Cancer Mortality, Radon Zone, Air Quality CPM
## vs
## SINGLE, UNIFIED database?

## create a database (if it doesn't exist)
if not database_exists(db.url):
    create_database(db.url)
## print(database_exists(db.url))

## insert data into database from Python
## For EDA only. Otherwise, this won't be useful for big data, of course
#cpmData.to_sql('cpmData', db, if_exists='replace')
lcmRadonData.to_sql('lungenvfac', db, if_exists='replace')

con = None
con = psycopg2.connect(database = dbname, user = user, host = host, password=pswd)




## geocodeLat
def geocodeLat(loc):
    gmaps = googlemaps.Client(key='AIzaSyBzz2U-OP788Nf3zqMRBJfcATKLcf6U3NE')
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    return lat
## geocodeLon
def geocodeLon(loc):
    gmaps = googlemaps.Client(key='AIzaSyBzz2U-OP788Nf3zqMRBJfcATKLcf6U3NE')
    geocode_result = gmaps.geocode(loc)
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    return lon




@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/output')
## @app.route('/output/<latitude><longitude>')
def output_page():
    ## Display the entire Database
    # queryLCMradon = """                                                                       
    #            SELECT index, county_x, latitude, longitude, average_deaths_peryear, lcar_radon_expected, lcar_radon_predicted, percent_error, radon_zone FROM lungenvfac;          
    #            """
    #print queryLCMradon
    #queryLCMradonResult = pd.read_sql_query(queryLCMradon,con)
    #print queryLCMradonResult
    #return render_template("results.html", num_results =queryLCMradonResult.shape[0],sites=queryLCMradonResult.to_html())

    ## INPUT (Text)
    inputUScounty = request.args.get('us_county')
    # check for user not entering anything
    # using the implicit booleanness of the empty list is quite pythonic, or so I hear on StackOverflow
    if not inputUScounty:
	return render_template('error.html')

    ## OUTPUT (Geocoded Coordinates)
    latitude = geocodeLat(inputUScounty)
    longitude = geocodeLon(inputUScounty)

    #queryLCMradon = """                                                                       
                #SELECT latitude, longitude, lcar_radon_predicted FROM lungenvfac WHERE latitude='$[latitude]' AND longitude='$[longitude]';          
                #"""
    # '$[person_name]'
    #print queryLCMradon
    #queryLCMradonResult = pd.read_sql_query(queryLCMradon,con)
    #print queryLCMradonResult
    
    ## For everyone who is trying to dynamically update their plots with some data sent from their HTML page: you can 1) send the data to Flask in an AJAX request (slide 15 in my web app tutorial), 
	## 2) get the data in the usual way, and generate the plot image data as a BytesIO object (slide 12), and finally 3) in the "success" callback function of the AJAX request from step 1, instead of 	## rendering HTML, render the image using the following code within that function:
	##$("#IMAGE_ID").attr("src", "data:image/png;base64,"+results);
	##(This will require jQuery, and an <img id="IMAGE_ID"> tag somewhere)
## small fix to the above: in step 2), instead of using send_file as in the tutorial, you should return the base64 encoded image itself. you add "import base64" to the top of your python script, and in  ## the function that will serve your plot, you return:

## return base64.b64encode(STRING_IO_OBJECT.getvalue())

## instead of calling send_file (and STRING_IO_OBJECT will be the object you plotted to in step 2) above)
    return render_template("index.html", latitude=latitude, longitude=longitude)
    #return render_template("index.html", latitude=latitude, longitude=longitude, lcmRadonResult=queryLCMradonResult.to_html())
