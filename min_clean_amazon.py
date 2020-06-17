import pandas as pd
import re
from html.parser import HTMLParser
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
#from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
#from nltk.stem import WordNetLemmatizer
import string

#stop_words = set(stopwords.words('english'))
punct = set(string.punctuation)


def text_cleaning(text):
    # converting HTML character codes to ASCII code
    parser = HTMLParser()
    text = parser.unescape(text)

    text = re.sub(r'<[^>]+>', '', text)  # removing HTML tags
    text = re.sub(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', '', text)  # removing hash-tags
    text = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', '',
                  text)  # removing URLs
    text = re.sub(r'(?:[\ufffd]+)', '', text)  # removing special characters
    text = ''.join(word for word in text if word not in punct)  # remove punctuation
    #text = re.sub('\n', ' ', text)  # remove new line
    #text = re.sub('@', '', text)  # remove @ sign
    #text = re.sub('’', '', text)
    #text = text.lower()  # lowercase all characters
    #text = word_tokenize(text)  # tonkenize words
    #text = [i for i in text if not i in stop_words]  # remove stop words
    #text = [stemmer.stem(word) for word in text]
    text = ''.join(text)

    return text


if __name__ == "__main__":
    df = pd.read_csv('amazon_scraped_data.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df = df[df['Reply Comments'].notnull()]

    df['Publish Time'] = df['Publish Time'].apply(lambda x: pd.to_datetime(x.strip(), format='%Y-%m-%d %H:%M:%S %Z'))

    df['Leading Comment'] = df['Leading Comment'].apply(lambda x: x.strip())
    df['Leading Comment'] = df['Leading Comment'].apply(lambda x: text_cleaning(x))

    df['Reply Comments'] = df['Reply Comments'].apply(lambda x: x.split('</div>'))
    df['Reply Comments'] = df['Reply Comments'].apply(lambda x: [text_cleaning(reply) for reply in x])

    df['Reply Times'] = df['Reply Times'].apply(lambda x: x.split('\\n')[1:-1])
    df['Reply Times'] = df['Reply Times'].apply(lambda x: [time.strip() for time in x if len(time) > 14])
    df['Reply Times'] = df['Reply Times'].apply(lambda x: [pd.to_datetime(time, format='%Y-%m-%d %H:%M:%S %Z') for time in x])

    df.to_csv('minClean_amazon.csv')