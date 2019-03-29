import collections
import matplotlib.pyplot as plt
import re

def read_data(filename):
  if filename is not None:
    with open(filename, 'r') as file:
      return file.read()
  return None

def parse(input):
  return input.split()

def pre_clean(t):
  # remove/strip/replace all punctuation from the parameter t
  t = t.replace('.', '')
  t = t.replace(',', '')
  t = t.replace('!', ' ')
  t = t.replace('?', '')
  t = t.replace('@', '')
  t = t.replace('--', ' ')
  t = t.replace('#', ' ')
  return t

def normalize(words):
  # ignore cases
  return [word.lower() for word in words]

def process_data(text):
  # call the different stages of
  # cleaning, parsing, normalizing
  # return the results as a list
  return normalize(parse(pre_clean(text)))

def top_n(tokens, n):
  counter = collections.Counter(tokens)
  return counter.most_common(n)

# VISUALIZATION

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