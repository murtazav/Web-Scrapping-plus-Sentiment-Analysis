
import numpy as np
import pandas as pd
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

df = pd.read_csv('ReviewData.csv')

corpus = []
words = []
for i in range(0, len(df)):
    review = re.sub('[^a-zA-Z]', ' ', df['Review Paragraph'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    words.extend(review)
    review = ' '.join(review)
    corpus.append(review)

nlp_words = nltk.FreqDist(words)

for word in nlp_words.most_common(10):
  print(word[0], sep=' ')
print(end='\n')

sid = SentimentIntensityAnalyzer()

pos = 0
neg = 0
maxi = -1
mini = 1
abs_min = 1
most_pos_rev = ''
most_neg_rev = ''
most_neu_rev = ''
for i in range(len(corpus)):
  score = sid.polarity_scores(corpus[i])['compound']
  if (score > 0):
    pos+=1
  else:
    neg+=1
  if (score > maxi):
    maxi = score
    most_pos_rev = df['Review Paragraph'][i]
  if (score < mini):
    mini = score
    most_neg_rev = df['Review Paragraph'][i]
  if (abs(score) < abs_min):
    abs_min = abs(score)
    most_neu_rev = df['Review Paragraph'][i]
percent_positive = pos / (pos+neg) * 100
percent_negative = neg / (pos+neg) * 100
print("percentage positive: ",percent_positive)
print("percentage_negative: ",percent_negative)
print("Most positive review: ",most_pos_rev)
print("Most negative review: ",most_neg_rev)
print("Most neutral review: ", most_neu_rev)

