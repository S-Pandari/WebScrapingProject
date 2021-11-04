from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import urllib.parse

baseURL = 'https://myanimelist.net/topanime.php'

# opening up connection
baseClient = uReq(baseURL)
pageHTML = baseClient.read()
baseClient.close()

pageSoup = soup(pageHTML, "html.parser")

containers = pageSoup.findAll("h3", {"class":"hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3"})

filename = "How Long To Watch Every Anime.csv"
f = open(filename, "w")

pageNum = 50

keepGoing = True

for go in range(2):

	for container in containers:

		#loads the anime's webpage on MAL
		anime_url = container.a["href"]
		anime_url = urllib.parse.urlsplit(anime_url)
		anime_url = list(anime_url)
		anime_url[2] = urllib.parse.quote(anime_url[2])
		anime_url = urllib.parse.urlunsplit(anime_url)

		animeClient = uReq(anime_url)
		animeHTML = animeClient.read()
		animeClient.close()
		animePageSoup = soup(animeHTML, "html.parser")

		#finds the title of the anime
		title = container.a.text

		#finds the table for the information
		data = animePageSoup.find("td")

		# this is the anime type (TV, Movie, etc.)
		animeType = data.find("span", string="Type:").find_next_sibling().text

		#this is the number of episodes
		numEpisodes = [int(s) for s in (data.find("span", string="Episodes:").find_parent().text).split() if s.isdigit()]

		#check is finished
		airing = data.find("span", string="Status:").find_parent().text
		finished = False
		if 'Finished Airing' in airing:
			finished = True

		#Genre List
		genreFinder = data.find("span", string="Genres:").find_parent().findAll("a")
		genreList = []
		for genres in range(len(genreFinder)):
			genreList.append(genreFinder[genres].text)
		genreString = ' '.join(map(str, genreList))

		#this is the time per episode
		timePerEpisode = [int(times) for times in (data.find("span", string="Duration:").find_parent().text).split() if times.isdigit()]
		if len(timePerEpisode) > 1:
			timePerEpisode[0] = (timePerEpisode[0] * 60) + (timePerEpisode[1])

		#this is the score
		score = data.find("span", string="Score:").find_next_sibling().text

		print("Title: " + title)
		print("Type: " + animeType)
		print("Number of Episodes: " + str(numEpisodes[0]))
		print("Finished Airing: " + str(finished))
		print("Genres: " + genreString)
		print("Time Per Episode: " + str(timePerEpisode[0]))
		print("Score: " + score)
		print("\n")

		importString = (title + "," + animeType + "," + str(numEpisodes[0]) + "," + str(finished) + "," + genreString + "," + str(timePerEpisode[0])+ "," + score + "\n")
		f.write(importString)

	baseURL = baseURL + "?limit=" + str(pageNum)
	pageNum = pageNum + 50

	# opening up connection
	baseClient = uReq(baseURL)
	pageHTML = baseClient.read()
	baseClient.close()

	pageSoup = soup(pageHTML, "html.parser")

	containers = pageSoup.findAll("h3", {"class":"hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3"})

f.close()