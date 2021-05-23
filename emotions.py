# Libraries 
import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Split the data between phrases and emotions
trainDataSet = pandas.read_csv("train.csv")
phrases = trainDataSet["phrase"]
feeling = trainDataSet["emotion"]

# List of all valid emotions
emotions = ["sadness", "anger", "love", "joy", "fear", "surprise"]

# Contains emotion values for each word 
vals = {
  # The format of values in this set is as follows:
  # "word": [sadnessValue, angerValue, loveValue, joyValue, fearValue, surpriseValue]
}

# Loop through all sentences and words in the dataset
for i in range(len(phrases)):
  words = phrases[i].split()
  emoti = feeling[i]
  # if i in range(10): print(words, emoti)
  for j in range(len(words)):
    # if i in range(10): print("word", words[j])
    if (words[j] in vals):
      vals[words[j]][emotions.index(emoti)] += 1
      # if i in range(10):
        # print("word", words[j], "emotions", emoti)
        # print("value", vals[words[j]])
        # print("vals", vals[words[j]][emotions.index(emoti)])
    else:
      vals[words[j]] = [0] * 6
      vals[words[j]][emotions.index(emoti)] += 1
      # if i in range(10):print("value", vals[words[j]])

# Printing dictionary 
# it = 0 # just printing 
# for key in vals: 
#   if it in range(10):
#     # print(key, vals[key])
#     it += 1

# Ratios calculation
it = 0 
for key in vals:
  totalSum = sum(vals[key])
  # if it in range(10): print(vals[key])
  for i in range(6):
    vals[key][i] /= totalSum
  it += 1
