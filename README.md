# Jeopardy Game

j-archive.com is a website that contains the compilation of all the jeopardy clues and answers fromt the show.

This python program utilises BeautifulSoup to scrape the J-Archive for all of the categories, values, clues, answers into a csv file
Using the scraped clues, Jeopardy clues can be played at random.

This repository consists of three python files.
EpisodeScraper.py creates a list of all of the hyperlinks to the individual games
This file needs to be run once before running Scraper.py
Scraper.py scrapes all of the individual games available and stores it in a csv file.

After running the scraping programs, the game program can be played.
GameDriver.py utilises the Arcade API.

This is intended solely for personal use
All credit for the clues goes to Jeopardy and j-archive.com
