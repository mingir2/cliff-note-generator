import collections
import matplotlib.pyplot as plt
import spacy
import numpy as np
import re
import requests
import urllib.parse

from nltk.util import bigrams

nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words

def read_remote(url):
  # assumes the url is already encoded (see urllib.parse.urlencode)
  response = requests.get(url)
  if response.status_code == requests.codes.ok: # that is 200
    return response.text
  return None
  
def build_google_drive_url(doc_id):
  baseurl = "https://drive.google.com/uc"
  params = {"export" : "download", "id" : doc_id}

  # build the url using baseurl
  # and the query parameters specified 
  # so that you can fetch it using
  # read_remote
  url = baseurl + "?" + urllib.parse.urlencode(params)
  return url

def get_data_from_cloud(drive_id):
  url = build_google_drive_url(drive_id)
  return read_remote(url)

def clean_data(text, title):
  # remove all header information up until the title of the book
  # remove all leading and trailing whitespace
  # return the cleaned text
  start = text.rfind(title)
  end = len(text)
  text = text[start:end]
  return text.strip()

def read_data_from_local(filename):
  if filename is not None:
    with open(filename, 'r') as file:
      return file.read()
  return None

def split_text_into_tokens(text):
  # skip single letter words (and numbers)
  # not match double hyphenated words (Aunt--Poly) (it will be two matches)
  # keep single hyphenated words (e.g. iron-will)
  # include the apostrophe in all of its possible uses.
  # strip off any leading and trailing apostrophes, keep the internal ones 
  regex = re.compile(r"['A-Za-z0-9]+-?['A-Za-z0-9]+")
  return [token.strip("'") for token in regex.findall(text)]

def normalize(tokens):
  # ignore cases
  return [token.lower() for token in tokens]

def top_n(tokens, n):
  # returns a list of tuples where each tuple contains the word followed by its count.
  # The count is the number of times the token occurs in tokens.
  # The parameter n is used to get the n most occurring tokens.
  counter = collections.Counter(tokens)
  return counter.most_common(n)
  
def load_stop_words(filename):
  # read filename and return a list of stopwords
  if filename is not None:
    with open(filename, 'r') as file:
      return file.read().split()
  return None

def get_titles(text):
  # tokenize honorifics (Dr. Mr. Mrs. Miss. Ms. Rev. Prof. Sir. etc)
  regex = re.compile(r"[A-Z]{1}[a-z]{1,3}[.]{1}[ ]{1}")
  title_tokens = [title.strip(' ').strip('.') for title in regex.findall(text)]
  regex = re.compile(r"[A-Z]{1}[a-z]{1,3}[ ]{1}")
  pseudo_titles = [title.strip(' ') for title in regex.findall(text)]
  return list(set(title_tokens) - set(pseudo_titles))

def find_characters(text, stoplist, top):
  # Tokenize and clean the text
  # Convert the list of tokens into a list of bigrams
  # Filter out all bigrams such that the first word in the bigram is a title and the second word is capitalized
  # Return the top bigrams as a list of tuples:  The first element is the bigram tuple, the second is the count
  titles = get_titles(text)
  grams = bigrams(split_text_into_tokens(text))
  grams_cap = [gram for gram in grams if gram[0][0].isupper() and gram[1][0].isupper()]
  grams_stoplist = [gram for gram in grams_cap if gram[0] not in stoplist and gram[1] not in stoplist]
  grams_title = [gram for gram in grams_stoplist if gram[0] in titles] 
  return top_n(grams_title, top)
  
def find_characters_nlp(text, top=15):
  # use spacy's Named Entity recognizer to pull out all people.
  doc = nlp(text)
  people = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]
  return top_n(people, top)

def split_into_chapters(text):
  # return an array whose elements are the text for each chapter
  # each element is trimmed of leading and trailing whitespace
  chapters = []
  rx = re.compile(r"CHAPTER ")
  curr = rx.search(text)
  
  while curr is not None:
    pos = curr.span()[1] # Starting search position
    chap = rx.search(text, pos)
    
    if chap is not None:
      idx = chap.span()
      chapters.append(text[pos:idx[0]])
    
    curr = chap
  chapters.append(text[pos:len(text)]) # Add the last chapter

  return chapters

def get_character_counts(chapters, names):
  # use the same function as in step 7
  counts = np.array([np.char.count(chapters, n) for n in names])
  counts = np.array([np.cumsum(n) for n in counts])
  counts = counts.T # get the data into the proper shape
  return counts