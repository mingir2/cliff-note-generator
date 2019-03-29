def read_data(filename):
  sentence = "YOU don't know about me without you have read a book by the name of The Adventures of Tom Sawyer; but that ain't no matter"
  if filename is not None:
    text = ""
    with open(filename, 'r') as fd:
      for line in fd:
        text += line
    return text
  return sentence

# PROCESS PIPELINE

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

# COMPUTE PIPELINE

def build_table(words):
  # builds a dictionary of counts
  table = {}
  for word in words:
    table[word] = table.setdefault(word, 0) + 1
  return table

def top_n(table, n):
  # sorts the table in reverse order based on the count.
  # return subset of the table of n size.
  return sorted(table.items(), key=lambda items: (-items[1], items[0]))[:n]

def compute_data(tokens, n):
  return top_n(build_table(tokens), n)