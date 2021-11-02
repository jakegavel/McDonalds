"""
Name: Jacob Gavel
CS230: SN5
Data: McDonald's
URL: Link to your web application online (see extra credit)

Description:  In this program the dataset for McDonalds stores is read in and used to create maps for the user.
The user is asked a variety of questions to help provide a base for the map and then the map can be interacted with to
see the features of the store and contact information about the store.
"""
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import streamlit as sl
import numpy as np
import random
import csv

dat = pd.read_csv("mcdonalds_clean1.csv")

sl.title("McDonald's Store Finder",)
sl.title("Store Locator")
rank = []
for rows in dat['state']:
    rank.append(0)

state = []
for states in dat["state"]:
    if states not in state:
        state.append(states)
state.sort()
state_select = sl.selectbox("Select your desired state: ", state)
count = 0
for states in dat['state']:
    if states == state_select:
        rank[count] += 3
    count += 1
cities = []
for city in (dat["city"][dat["state"] == state_select]):
    if city not in cities:
        cities.append(city)
cities.sort()
cities.append("Not listed")
city_select = sl.selectbox("Selected your desired city: ", cities)
count = 0
for city in dat['city']:
    if city == city_select:
        rank[count] += 2
    count += 1

def variants():

    sl.title("Store Ranker")

    play = sl.radio("Are you coming with children?", ('Y', 'N'))

    count = 0
    for vals in dat["playplace"]:
        if play == vals:
            rank[count] += 1
        count += 1

    thru = sl.radio("Are you in a rush?", ('Y', 'N'))

    count = 0
    for vals in dat["driveThru"]:
        if thru == vals:
            rank[count] += 1
        count += 1

    arch = sl.radio("Do you have an Archcard gift card?", ('Y', 'N'))

    count = 0
    for vals in dat["archCard"]:
        if arch == vals:
            rank[count] += 1
        count += 1

    wifi = sl.radio("Are you bringing your devices to the store?", ('Y', 'N'))

    count = 0
    for vals in dat["freeWifi"]:
        if wifi == vals:
            rank[count] += 1
        count += 1

    choice = []
    for choices in dat["storeType"]:
        if choices not in choice:
            choice.append(choices)
    store_type = sl.selectbox("What else must be around the store? ", choice)
    count = 0
    for vals in dat["storeType"]:
        if store_type == vals:
            rank[count] += 1
        count += 1

    dat["Rank"] = rank
    df = dat.dropna()
    df.to_csv('mcdonalds_clean1.csv',sep=',', index=False)
def maps(state_select):

    sl.title("McDonald's In Your Area")

    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/200px-McDonald%27s_Golden_Arches.svg.png"

    icon_data = {"url": ICON_URL, "width": 242, "height": 242, "anchorY": 242,}
    dat["icon_data"] = ""
    for i in dat.index:
        dat["icon_data"][i] = icon_data

    sl.pydeck_chart(pdk.Deck(
    layers=[
            pdk.Layer(
            type="IconLayer",
            data=dat,
            get_icon='icon_data',
            get_size=5,
            size_scale=10,
            get_position='[lon, lat]',
            pickable=True, billboard=True),
            pdk.Layer(
            type="ScreenGridLayer",
            data=dat,
            pickable=False,
            cell_size_pixels=25,
            color_range=[
                [25, 0, 0, 25], [50, 0, 0, 50], [76, 0, 0, 76], [101, 0, 0, 101], [127, 0, 0, 127],[152,0,0,152], [178, 0, 0, 178], [203, 0, 0 , 203], [255, 0, 0, 255]],
            opacity=0.4,
            get_position='[lon, lat]',
            get_weight= 'Rank > 0 ? Rank: 0')],
        map_style='mapbox://styles/mapbox/light-v9',
        mapbox_key= 'pk.eyJ1IjoiamdhdmVsIiwiYSI6ImNraXM0bnRxNDI5d2gydHBkamVucm16YjUifQ.MAPFIRT_g4Sl9sLv818KPg',
        initial_view_state=pdk.ViewState(
            latitude=np.average(dat['lat'][dat['state'] == state_select]),
            longitude=np.average(dat['lon'][dat['state'] == state_select]),
            zoom=7, pitch=20),
        tooltip={
            "html": "Store Number:<br/> <b>{storeNumber}</b> <br/> City and State:<br/> <b>{city}</b> {state} </b>, {zip}"
            " </b> <br/> Store URL:<br/> <b>{storeUrl}</b> <br/> Store Phone number:<br/> <b>{phone}</b>"
            "</b> <br/> Rating:<br/> <b>{Rank}<b> out of 10 </b> <br/>",
            "style": {"backgroundColor": 'crimson',
            "color": "white"}}))

def plot(state_select, rank):
    sl.title("Data Analysis")

    fig, chart = plt.subplots()
    chart.hist(dat['Rank'][state_select == dat['state']], bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11], color='gold')
    chart.xaxis.set_label_text("Rating of the Stores")
    chart.yaxis.set_label_text("Frequency of the Stores")
    chart.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    chart.set_facecolor('crimson')
    fig.suptitle(f"Histogram of the Ranked Stores in {state_select}")
    sl.pyplot(fig)

    max_state = []
    max_city = []
    min_state = []
    min_city = []
    max_rank = dat['Rank'].max()
    min_rank = dat['Rank'].min()
    for i in dat.index:
        if dat['Rank'][i] == max_rank:
            max_state.append(dat['state'][i])
            max_city.append(dat['city'][i])
        if dat['Rank'][i] == min_rank:
            min_state.append(dat['state'][i])
            min_city.append(dat['city'][i])
    rand_select = random.randint(0, len(max_state) - 1)
    rand_selects = random.randint(0, len(min_state) - 1)
    if len(max_state) == 1:
        pronoun1 = "is"
        s1 = ""
    else:
        pronoun1 = "are"
        s1 = "s"
    if len(min_state) == 1:
        pronoun2 = "is"
        s2 = ""
    else:
        pronoun2 = "are"
        s2 = "s"
    sl.subheader(f"There {pronoun1} {len(max_state)} store{s1} with the highest rating of {max_rank}, one such store is in {max_city[rand_select]}, {max_state[rand_select]}")
    sl.subheader(f"There {pronoun2} {len(min_state)} store{s2} with the lowest rating of {min_rank}, one such store is in {min_city[rand_selects]}, {min_state[rand_selects]}")

    total = 0
    count = 1
    for vals in rank:
        total += vals
        count += 1
    mean= total / count

    return sl.subheader(f"Mean rating = {mean}")
def main():
    variants()
    maps(state_select)
    plot(state_select, rank)
main()
