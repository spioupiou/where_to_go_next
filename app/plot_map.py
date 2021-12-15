import folium
import random
import csv
import base64
from app.dictionary import jp_cities
from folium import Map
from folium.plugins import LocateControl, MarkerCluster, Fullscreen


def encode64(pic):
    encoded = base64.b64encode(open(pic, 'rb').read()).decode()
    return encoded


def basemap_layer():
    m = folium.Map(location=[39,136], tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
                   attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
                   prefer_canvas=True,
                   control_scale=True,
                   zoom_start=5,
                   min_zoom=4,
                   max_zoom=20,
                   width=800,
                   height=600)
    LocateControl(auto_start=False).add_to(m)
    return m


def map_plot(m, dico):
    for city, details in dico.items():
        name = city
        coordinates = (details['lat'], details['lon'])
        pref = details['pref']
        picture = details['picture']
        comments = details['comments']

        if picture != 'NULL':
            encoded = encode64(picture)

            cplx_html = f'''
            <div class="content">
                <img border="0" style="padding-right: 15px" src="data:image/jpg;base64,{encoded}">
                <div class="text">
                    <p>
                        <b><span style="font-family: Arial; font-size: 17px;">{name}</span></b><br>
                        <span style="font-family: Arial; font-size: 14px;">{pref} Prefecture</span>
                        <p style="font-family: Arial; font-size: 12px; text-align: justify;">{comments}</p>
                    </p>
                </div>
            </div>'''

            marker = make_cplx_marker(coordinates, cplx_html, name)
            marker.add_to(m)

        else:
            simple_html = f'''
            <div class="content">
                <div class="text">
                    <p>
                        <b><span style="font-family: Arial; font-size: 17px;">{name}</span></b><br>
                        <span style="font-family: Arial; font-size: 14px;">{pref} Prefecture</span>
                        <p style="font-family: Arial; font-size: 12px;">{comments}<p>
                    </p>
                </div>
            </div>'''

            marker = make_simple_marker(coordinates, simple_html, name)
            marker.add_to(m)


def make_cplx_marker(location, html, tooltip):
    iframe = folium.IFrame(html, width=315, height=300)
    popup = folium.Popup(iframe, max_width=1000)
    MyMarker = folium.Circle(location=location, popup=popup, tooltip=tooltip, radius=1600,
                             stroke=False, fill=True, fill_color='#CEFA05', fill_opacity=1)
    return MyMarker


def make_simple_marker(location, html, tooltip):
    iframe = folium.IFrame(html, width=150, height=75)
    popup = folium.Popup(iframe, max_width=1000)
    MyMarker = folium.Circle(location=location, popup=popup, tooltip=tooltip, radius=1600,
                             stroke=False, fill=True, fill_color='#CEFA05', fill_opacity=1)
    return MyMarker


def random_marker(m, region):
    icon = folium.Icon(icon="paper-plane", prefix="fa", color='green')

    if region == "All":
        with open('app/data/jp.csv', 'r') as database:
            reader = csv.reader(database)
            next(reader)
            mydict = {row[0]:(float(row[1]), float(row[2])) for row in reader}

        random_city = random.choice(list(mydict.keys()))
        random_coordinates = mydict[random_city]

        random_marker = folium.Marker(location=random_coordinates, tooltip=random_city, icon=icon)
        random_marker.add_to(m)

    else:
        with open('app/data/%s.csv' % region, 'r') as database:
            reader = csv.reader(database)
            next(reader)
            mydict = {row[0]:(float(row[1]), float(row[2])) for row in reader}

        random_city = random.choice(list(mydict.keys()))
        random_coordinates = mydict[random_city]

        random_marker = folium.Marker(location=random_coordinates, tooltip=random_city, icon=icon)
        random_marker.add_to(m)


def save_map(m):
    m.save('app/templates/MyMap.html')
