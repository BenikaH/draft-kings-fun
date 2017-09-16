import requests
import csv
from bs4 import BeautifulSoup
from draft_kings_fun.nba.data_cleaning_constants import RENAMES

NUMBER_FIRE_URL = 'http://www.numberfire.com/nba/daily-fantasy/'


def scrape():
    playernames = ['playername']
    points = ['points']

    s = requests.session()
    s.post('{}set-dfs-site'.format(NUMBER_FIRE_URL), data=dict(site=4))
    r = s.get('{}daily-basketball-projections'.format(NUMBER_FIRE_URL))

    soup = BeautifulSoup(r.content, 'html.parser')

    player_names = soup.find_all("a", {"class": "full"})
    player_fp = soup.find_all("td", {"class": "fp active"})

    for i in player_names:
        name = i.get_text().strip()
        renames = \
            [n['dk_name'] for n in RENAMES
             if n['name'] == name]
        if renames:
            name = renames[0]

        playernames.append(name)
    for i in player_fp:
        points.append(i.get_text().strip())

    players = [list(i) for i in zip(playernames, points)]
    with open('data/current-projections.csv', 'w') as fp:
        w = csv.writer(fp)
        w.writerows(players)
