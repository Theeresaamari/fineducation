# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TvQWwJWbQRjAmx127gF4vhj-PK3mGr0S
"""

pip install flask flask-wtf

# redirect
# url_for
# request.form

"""Now let’s hop over to server.py and code that “/submit” route.

But for the sake of learning, we’re going to allow anyone to submit anything and store it directly to our CSV flat file database.

To start, we’re going to make our “/submit” route able to handle both GET requests (when the user simply goes to a webpage) and POST requests (when the user is sending data from a form). Add this code right below your index route:
"""

@app.route("/submit", methods=["GET", "POST"])   #make summit handle GET regquest and POST regquest
def submit():
  if request.method == "GET":
    return redirect(url_for('index'))  #if user treis to GET the submit page, they are redirected to the index route

"""If the user tries to GET the submit page, they are simply redirected to the index route (redirect and url_for have already been imported for you from Flask).
However, if the user POSTs to the submit page…
"""

elif request.method == "POST":
    userdata = dict(request.form)    #route sammelt daten von Form Data
    city = userdata["city"][0]
    attraction = userdata["attraction"][0]
    gif_url = userdata["gif"][0]
    if len(city) < 2 and len(attraction) < 3 and (len(gif_url) < 10 or "gif" not in gif_url):   #check if valid
      return "Please submit valid data."
    with open('.data/places.csv', mode='a') as csv_file:    #open secret data
      data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      data.writerow([city, attraction, gif_url])
  return "Thank you!"

"""For a POST request, the route gathers the place’s city, attraction, and gif URL from the form data (accessed by request.form — request has been imported for you).
Then it checks if the data is valid primarily by string length and also checking if the gif URL contains “gif.” If the data is not valid, we return an error message.
If the data is valid, we open our secret .data/places.csv file in the “append” mode and create a CSV writer object. Then we write new row on the CSV that contains the city, attraction, and gif.
Finally, if all goes well, we return “Thank you!”
Test out your new route by inputting a new city!

To read the CSV file, we’ll need to import Python’s csv module at the top of server.py:
"""

import csv

"""Then, to read and process the CSV, we revise the index route in server.py like so:"""

@app.route("/")
def index():
  with open('.data/places.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    first_line = True
    places = []
    for row in data:
      if not first_line:
        places.append({
          "city": row[0],
          "attraction": row[1],
          "gif_url": row[2]
        })
      else:
        first_line = False
  return render_template("index.html", places=places)