# this program compiles the data from all of the episodes
# available on the J-archive website and stores it
# in the jeopardy.csv file
# Please read the note commented in line 197
# to run this program in sections

import requests
import time
from bs4 import BeautifulSoup
import pandas as pd


def get_values(url):
    categories = []
    answers = []
    values = []
    clues = []

    # get html of game
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")
    time.sleep(1)

    try:
        # ROUND ONE
        table = soup.find('div', {'id': 'jeopardy_round'})
        table_header = table.find_all('td', class_='category')

        cats = []

        # collect categories
        for x in range(0, 6):
            cat = table_header[x]
            cats.append(cat.get_text().replace('\n', ''))
        # make the number of categories match the number of clues
        for x in range(0, 5):
            categories += cats
        # collect question information
        table_body = table.find_all('td', class_='clue')
        for x in range(0, 30):

            # collect values
            try:
                value = table_body[x].find('td', class_='clue_value').get_text()
                value.replace("$", "")
            except:
                value = "0"

            # collect clues
            try:
                clue = table_body[x].find('td', class_='clue_text').get_text()
            except:
                clue = "NaN"

            # collect answers
            try:
                ans = table_body[x].find('div', onmouseover=True)
                answer = ans['onmouseover']
                begin = answer.index('correct_response\">') + 18
                answer = answer[begin::]
                end = answer.index('</em')
                answer = answer[:end:]
            except:
                answer = "NaN"

            values.append(value)
            clues.append(clue)
            answers.append(answer)
    except:
        print("No round one")

    try:
        # ROUND TWO
        table = soup.find('div', {'id': 'double_jeopardy_round'})
        table_header = table.find_all('td', class_='category')

        cats = []
        # collect categories
        for x in range(0, 6):
            cat = table_header[x]
            cats.append(cat.get_text().replace('\n', ''))

        # make the number of categories match the number of clues
        for x in range(0, 5):
            categories += cats

        # collect question information
        table_body = table.find_all('td', class_='clue')
        for x in range(0, 30):

            # collect values
            try:
                value = table_body[x].find('td', class_='clue_value').get_text()
                value.replace("$", "")
            except:
                value = "0"

            # collect clues
            try:
                clue = table_body[x].find('td', class_='clue_text').get_text()
            except:
                clue = "NaN"

            # collect answers
            try:
                ans = table_body[x].find('div', onmouseover=True)
                answer = ans['onmouseover']
                begin = answer.index('correct_response\">') + 18
                answer = answer[begin::]
                end = answer.index('</em')
                answer = answer[:end:]
            except:
                answer = "NaN"

            values.append(value)
            clues.append(clue)
            answers.append(answer)
    except:
        print("No Double Jeopardy")

    try:
        # FINAL JEOPARDY
        table = soup.find('table', {'class': 'final_round'})

        # collect category
        table_header = table.find('td', class_='category')
        categories.append(table_header.get_text().replace('\n', ''))
        # create distinct value for final jeopardy roung
        values.append('-1')
        # collect clue
        try:
            clue = table.find('td', class_='clue').get_text()
            clue = clue.replace('\n', '')
        except:
            clue = "NaN"
        clues.append(clue)
        # collect answer
        try:
            ans = table.find('div', onmouseover=True)
            answer = ans['onmouseover']
            begin = answer.index('<em') + 31
            end = answer.index('</em')
            answer = answer[begin:end:]
        except:
            answer = "NaN"
        answers.append(answer)
    except:
        print("No final jeopardy")
    # clean data
    for x in range(0, len(answers)):
        answers[x] = answers[x].replace('<i>', '')
        answers[x] = answers[x].replace('</i>', '')

    for x in range(0, len(clues)):
        try:
            if '(' in clues[x]:
                begin = clues[x].index('(')
                end = clues[x].index(')')
                clues[x] = clues[x].replace(clues[x][begin:end + 1:], "")
                clues[x] = clues[x].strip()
        except:
            print(clues[x])
        try:
            if '(' in categories[x]:
                begin = categories[x].index('(')
                end = categories[x].index(')')
                categories[x] = categories[x].replace(categories[x][begin:end + 1:], "")
                categories[x] = categories[x].strip()
        except:
            print(categories[x])

    # create data frame
    data = pd.DataFrame({
        'Category': categories,
        'Value': values,
        'Clue': clues,
        'Answer': answers,
    })

    try:
        # clean data
        data['Value'] = data['Value'].str.extract('(\d+)').astype(int)
    except:
        print("Empty Game")
    data = data[data.Value != 0]
    data = data[data.Clue != '=']

    return data


# Run this file after running EpisodeScraper

# Collect Data
episodes = pd.read_csv("episodes.csv")
episodes = episodes.links
count = 0

# Note: the link and place in the episode array are printed out
# so that you can run the program in sections and pick up
# where the previous iteration left off
# to do so, change the line 196 below to
# for link in episodes[ (last count number printed) + 1 ::]:
for link in episodes:
    df = get_values(link)
    df.to_csv('jeopardy.csv', mode='a', header=False)
    print(link)
    print(count)
    count += 1
