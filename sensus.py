import sys
from flask import Flask, request, render_template
import json
import results

app = Flask(__name__)

@app.route('/')
def home():
    with open("static/us-states.json") as d:
        data = json.load(d)
        return render_template('index.html', data=data)

@app.route('/', methods=['POST'])
def form_post():
    keyword = request.form['name']
    with open("static/us-states.json") as d:
        data = json.load(d)

        results = results.main(keyword.upper())
        for key, value in results.iteritems():
            data["features"][value[0]]["properties"]["density"] = value[1]

        return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
