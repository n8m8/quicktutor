from flask import Flask, render_template, jsonify, request
from flask_googlemaps import GoogleMaps

app = Flask(__name__)

# This is simple search for location, sends to a different link. The other html
# file is more accruate since it doesn't reroute, just need to add a selection
# feature so we can extract logitude+latitude for it

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

@app.route("/", methods=["GET"])
def retreive():
    return render_template('maptest.html')

@app.route("/sendRequest/<string:query>")
def results(query):
    search_payload = {"key":AIzaSyCHDS9VJKpYw2MS6LGHMJshSt9WN4AMxgM, "query":query}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()

    place_id = search_json["results"][0]["place_id"]

    details_payload = {"key":AIzaSyCHDS9VJKpYw2MS6LGHMJshSt9WN4AMxgM, "placeid":place_id}
    details_resp = requests.get(details_url, params=details_payload)
    details_json = details_resp.json()

    url = details_json["result"]["url"]
    return jsonify({'result' : url})

# setting key as config
app.config['GOOGLEMAPS_KEY'] = 'AIzaSyCHDS9VJKpYw2MS6LGHMJshSt9WN4AMxgM'

if __name__ == "__main__":
    app.run(debug=True)

# init extension
GoogleMaps(app)
