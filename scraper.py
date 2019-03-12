# importing libraries
import pandas as pd
import numpy as np
from requests import get  # Retrieving information in a website
from bs4 import BeautifulSoup  # Extracting data
from time import time  # calculate the time
from time import sleep  # pause the loop
from random import randint  # Randomize sleep time
from IPython.core.display import clear_output  # Stack the output
from warnings import warn  # Warn when something goes wrongxs

pages = [str(i) for i in range(1, 152, 50)]
years_url = [str(i) for i in range(1968, 2019)]

names = []
years = []
imdb_ratings = []
metascores = []
votes = []
genre = []
runtime = []
directors = []
actors = []
description = []
rank = []
gross = []

start_time = time()
requests = 0

# for every year
for year_url in years_url:

    # For every page
    for page in pages:

        # Make a get request
        response = get('https://www.imdb.com/search/title?title_type=feature&release_date=' + year_url +
                       '-01-01,' + year_url + '-12-31&sort=num_votes,desc&start=' + page + '&ref_=adv_nxt')

        # Pause the loop for 8~15 seconds
        sleep(randint(8, 15))

        # observe the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
        # Stack the output
        clear_output(wait=True)

        # Put a warning if != 200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is over 115
        if requests > 205:
            warn('Number of requests was greater than expected.')
            break

            # Parse the url with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Creating movie container for all 50 titles
        movie_containers = page_html.find_all('div', class_='lister-item mode-advanced')

        # For every title
        for container in movie_containers:

            # Getting the name
            name = container.h3.a.text
            names.append(name)

            # Getting the year
            try:
                year = int(container.h3.find('span', class_='lister-item-year text-muted unbold').text.strip('(IIIVX) '))
                years.append(year)
            except:
                year_null = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year_null)

            # Getting the rating
            imdb = float(container.strong.text)
            imdb_ratings.append(imdb)

            # Getting the Metascore if the value exist
            if container.find('div', class_='ratings-metascore') is not None:
                m_score = container.find('span', class_='metascore').text
                metascores.append(int(m_score))
            # Else assign in the NaN
            else:
                m_null = np.NaN
                metascores.append(m_null)

            # Getting the number of votes
            vote = container.find('span', attrs={'name': 'nv'})['data-value']
            votes.append(int(vote))

            # Getting the genre
            genr = container.find('span', 'genre').text.strip()
            genre.append(genr)

            # Getting the duration of the movie
            try:
                duration = [float(s) for s in container.find('span', 'runtime').text.split() if s.isdigit()][0]
                runtime.append(duration)
            except:
                dur_null = np.NaN
                runtime.append(dur_null)

            # Getting the director
            try:
                director = ''.join([str(s) for s in
                                    container.find_all('p', '')[2].text.replace('\n', '').strip('\n').split('|')[
                                        0].split(':')[1:]])
                directors.append(director)
            except:
                d_null = np.NaN
                directors.append(d_null)

            # Getting the actors
            try:
                actor = ''.join([str(s) for s in
                                 container.find_all('p', '')[2].text.replace('\n', '').strip('\n').split('|')[1].split(
                                     ':')[1:]])
                actors.append(actor)
            except:
                a_null = np.NaN
                actors.append(a_null)
            # Getting the description
            desc = container.find_all('p', class_='text-muted')[1].text.strip()
            description.append(desc)

            # Getting the rank
            ranks = int(container.find('span', 'lister-item-index unbold text-primary').text.replace('.', ''))
            rank.append(ranks)

            # Getting the gross if it exist
            try:
                gros = int(container.find_all('span', attrs={'name': 'nv'})[1]['data-value'].replace(',', ''))
                gross.append(gros)
            # Else sign to NaN
            except:
                gros_null = np.NaN
                gross.append(gros_null)

end_time = time()
# Print out how many seconds it took to run the loop
print(end_time - start_time)

# storing data
df_imdb = pd.DataFrame({'rank': rank,
                        'name': names,
                        'year': years,
                        'rating': imdb_ratings,
                        'metascore': metascores,
                        'votes': votes,
                        'revenue': gross,
                        'genre': genre,
                        'runtime': runtime,
                        'directors': directors,
                        'actors': actors,
                        'description': description})

df_imdb.to_csv('imdb_data.csv')
