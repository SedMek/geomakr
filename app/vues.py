import argparse

import requests
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

from app.config import ncfa, game_specs, BASE_URL, API_SUFFIX, GAME_SUFFIX

@app.route('/')
def selection():
    return render_template("selection.html")

@app.route('/gen', methods=["GET"])
def generate():
        if request.method == "GET":
            map = request.args.get("map") or "world"
            timelimit = request.args.get("timelimit") or 90
            links = get_links(map, timelimit, 1)
            return redirect(links[0])
        else:
            return redirect(url_for("selection"))


def get_links(map, timelimit, nb):
    map = map or "world"
    timelimit = timelimit or 90
    nb = nb or 1
    links = []
    for i in range(nb):
        response = requests.post(BASE_URL+API_SUFFIX, cookies={"_ncfa": ncfa}, data = game_specs(map, timelimit))
        if response.status_code == 200:
            links.append(BASE_URL+GAME_SUFFIX+response.json().get("token"))
        else:
            raise Exception("An error has occured")
    return links

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--map", help="name of the map as displayed on geoguessr url", type=str, required=False)
#     parser.add_argument("--time", help="Time limit of each round", type=int, required=False)
#     parser.add_argument("--nb", help="Number of generated links", type=int, required=False)

#     args = parser.parse_args()
#     main(map=args.map, timelimit=args.time, nb=args.nb)
