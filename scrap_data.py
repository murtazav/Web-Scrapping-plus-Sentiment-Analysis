import requests
from bs4 import BeautifulSoup
import pandas as pd

ls_sites = []
ls_ratings = []
ls_titles = []
ls_dates = []
ls_reviews = []

for j in range(22):
	if j==0:
		a=''
	else:
		a='-or'+str(j*10)
	site ='https://www.tripadvisor.in/Restaurant_Review-g304551-d13388460-Reviews'+a+'-Kitchen_With_A_Cause-New_Delhi_National_Capital_Territory_of_Delhi.html'
	result = requests.get(site)
	#print(result.status_code)  
	src = result.content
	soup = BeautifulSoup(src, 'html.parser') 
	tag = soup.find_all('div',attrs={'class':'review-container'})
	#print(len(tag))

	#print(tag[0].find_all('span')[1]['class'][1])

	for i in range(len(tag)):
		rating = int((tag[i].find_all('span')[1]['class'][1]).split('_')[-1])/10
		title = tag[i].find_all('span',attrs={'class':"noQuotes"})
		review_date = tag[i].find_all('span',attrs={'class':'ratingDate'})
		review = tag[i].find_all('p', attrs={'class':'partial_entry'})
		ls_sites.append(site)
		ls_ratings.append(rating)
		ls_titles.append(title[0].find(text=True))
		ls_dates.append(review_date[0]['title'])
		ls_reviews.append(review[0].find(text=True))

data = {'Site':ls_sites,
		'Rating':ls_ratings,
		'Review Title':ls_titles,
		'Review Date':ls_dates,
		'Review Paragraph':ls_reviews}

df = pd.DataFrame(data)
#print(df.head())
df.to_csv('ReviewData.csv', index=False)
print("Successfuly Scraped")