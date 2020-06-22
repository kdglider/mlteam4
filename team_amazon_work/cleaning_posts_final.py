import pandas as pd
import re
from html.parser import HTMLParser
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import string

stop_words = set(stopwords.words('english'))
punct = list(set(string.punctuation))
punct.append('“')
punct.append('”')
stemmer = PorterStemmer()


def text_cleaning(text):
    # converting HTML character codes to ASCII code
    parser = HTMLParser()
    text = parser.unescape(text)

    text = re.sub(r'<[^>]+>', '', text)  # removing HTML tags
    text = re.sub(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', '', text)  # removing hash-tags
    text = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', '',text)  # removing URLs
    text = re.sub(r'(?:[\ufffd]+)', '', text)  # removing special characters
    text = ''.join(word for word in text if word not in punct)  # remove punctuation
    text = re.sub('\n', ' ', text)  # remove new line
    text = re.sub('@', '', text)  # remove @ sign
    text = re.sub('’', '', text)
    text = text.lower()  # lowercase all characters
    text = word_tokenize(text)  # tonkenize words
    text = [i for i in text if not i in stop_words]  # remove stop words
    # text = [stemmer.stem(word) for word in text]
    text = ' '.join(text)

    return text


if __name__ == "__main__":
    df = pd.read_csv('amazon_scraped_data.csv')
    print('data imported')

    df.drop(['Unnamed: 0','Link','Reply Times'],axis=1,inplace=True)
    print('unnecessary columns dropped')

    df['Publish Time'] = df['Publish Time'].apply(lambda x: pd.to_datetime(x.strip(), format='%Y-%m-%d %H:%M:%S %Z'))
    df['Publish hour'] = df["Publish Time"].apply(lambda x: x.hour)
    print('publish time cleaned')

    df['Title'] = df['Title'].apply(lambda x: text_cleaning(x))
    print('title column cleaned')

    df['Leading Comment'] = df['Leading Comment'].apply(lambda x: x.strip())
    df['Leading Comment'] = df['Leading Comment'].apply(lambda x: text_cleaning(x))
    print('leading comment column cleaned')

    df['Reply Comments'] = df['Reply Comments'].apply(lambda x: x.split('</div>'))
    df['Reply Comments'] = df['Reply Comments'].apply(lambda x: [text_cleaning(reply) for reply in x])
    print('reply comments column cleaned')

    df['Reply Authors'] = df['Reply Authors'].apply(lambda x: word_tokenize(x))
    df['Reply Authors'] = df['Reply Authors'].apply(lambda x: [word for word in x if word not in punct])
    df['Reply Authors'] = df['Reply Authors'].apply(lambda x: [re.sub('\'', '', x[i]) for i in range(len(x))])
    print('reply authors column cleaned')
    df['num_Reply_Authors'] = df['Reply Authors'].apply(lambda x: len(x))

    df.to_csv('cleaned_data.csv')
    print('finished data cleaning, data has been exported!')