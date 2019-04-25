import requests
from  bs4 import BeautifulSoup
import json


# function that crawls the website. Take in a url and scrapes the website accordingly
def tournament_spider(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="lxml")

    # get the tournament name
    tournament_name = soup.title.string.split('-')[0].encode("utf-8").strip()
    tournament_json = {}
    team_players = {}
    all_players = []

    # get start and end dates
    boxes = soup.findAll('div', {'class': ['infobox-cell-2', 'infobox-description']})
    start_date = boxes[17].string
    end_date = boxes[19].string

    # parse the teams and each player inside the team
    for team in soup.findAll('div', {'class':['teamcard toggle-area', 'toggle-area-1']}):
        teamname = team.contents[0].next.string.encode("utf-8").strip()
        teammates = [team.findAll('td')[x].contents for x in range(6)]
        teammates = [x[len(x)-2].get('title') for x in teammates]
        team_players[teamname] = teammates
        all_players.append(teammates)

    #build the JSON to be returned
    tournament_json['name'] = tournament_name
    tournament_json['start_date'] = start_date
    tournament_json['end_date'] = end_date
    tournament_json['teams'] = team_players

    with open(tournament_name+'.json', 'w') as outfile:
        json.dump(tournament_json, outfile)


tournament_spider('https://liquipedia.net/leagueoflegends/World_Championship/2018')
