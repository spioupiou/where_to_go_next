from flask import Flask, jsonify, render_template, request
from app.plot_map import basemap_layer, map_plot, random_marker, save_map
from app.dictionary import jp_cities

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

REGIONS = ["All", "Hokkaido", "Tohoku", "Kanto", "Chubu", "Kansai", "Chugoku", "Shikoku", "Kyushu (incl. Okinawa)"]

@app.route("/")
def index():
    MyMap = basemap_layer()
    map_plot(MyMap, jp_cities)
    save_map(MyMap)
    return render_template("index.html", regions=REGIONS)

@app.route("/randomize",  methods=["GET", "POST"])
def randomize():
    if request.method == "GET":
        MyMap = basemap_layer()
        map_plot(MyMap, jp_cities)
        save_map(MyMap)
        return render_template("index.html", regions=REGIONS)        

    else:
        MyMap = basemap_layer()
        map_plot(MyMap, jp_cities)
        region = request.form.get("region")
        random_marker(MyMap, region)
        save_map(MyMap)
        return render_template("randomize.html", regions=REGIONS)
