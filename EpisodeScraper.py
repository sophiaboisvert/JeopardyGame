# this program compiles the links to all of the episodes
# available on the J-archive website and stores it
# in the episodes.csv file

import requests
import time
from bs4 import BeautifulSoup
import pandas as pd


def get_links(first, second):
    # get html
    results = requests.get(first + second)
    soup = BeautifulSoup(results.text, "html.parser")
    time.sleep(1)

    results = []

    # collect links
    links = soup.find('div', {'id': 'content'})
    links = links.find_all('a')
    for hyp_link in links:
        results.append(hyp_link['href'])
    return results


url = "http://www.j-archive.com/"
add = "listseasons.php"

# collect list of seasons
seasons = get_links(url, add)

# collect list of episodes
episodes = []
for link in seasons:
    episodes += get_links(url, link)

# clean data
for x in range(0, len(episodes)):
    if 'game_id' not in episodes[x]:
        episodes[x] = 'NaN'
    elif 'https' not in episodes[x]:
        episodes[x] = "http://www.j-archive.com/" + episodes[x]
df = pd.DataFrame({
    'links': episodes
})
df = df[df.links != 'NaN']

# save to file
df.to_csv('episodes.csv')
