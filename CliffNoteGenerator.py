import collections
import matplotlib.pyplot as plt
import re

def read_data(filename):
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

def bi_grams(tokens):
  # returns a list of tuples.
  # This function moves a sliding window of size 2 over tokens, and creates a list of bigrams.
  # tuples: each tuple has two elements both of them tokens.
  return [(tokens[i-1], tokens[i]) for i in range(1,len(tokens))]
  
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
  grams = bi_grams(split_text_into_tokens(text))
  grams_cap = [gram for gram in grams if gram[0][0].isupper() and gram[1][0].isupper()]
  grams_stoplist = [gram for gram in grams_cap if gram[0] not in stoplist and gram[1] not in stoplist]
  grams_title = [gram for gram in grams_stoplist if gram[0] in titles] 
  return top_n(grams_title, top)

def visualize_high(tuples, filename):
  # Bar chart with highest being red.
  labels = []
  counts = []
  for t in tuples:
    labels.append(t[0])
    counts.append(t[1])
    
  x_pos = range(len(labels))
  
  # use the object API
  fig = plt.figure()
  ax  = fig.add_subplot(111) 
  
  # create the bars with color
  ax.bar(x_pos, counts, color=(['red'] + ['blue' for i in range(len(labels)-1)]))
  
  ax.set_xlabel('word',  fontsize=12)
  ax.set_ylabel('count', fontsize=12)
  
  ax.set_xticks(x_pos)
  ax.set_xticklabels(labels, fontsize=8, rotation=30)
  ax.set_title('Word Usage')
  
  fig.savefig(filename)

  # Close plt to prevent duplicate plot in jupyter notebook
  plt.close()
  
  # return the figure
  # allows the caller to customize
  # do NOT return plt
  return fig