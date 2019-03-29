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

def visualize_high(tuples, filename):
  # Bar chart with highest being red
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