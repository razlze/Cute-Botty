import pandas
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# import seaborn as sns
# %matplotlib inline

random_seed = 932874
numpy.random.seed(random_seed)

# from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix
# import itertools

# from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
# from keras.optimizers import RMSprop
# from keras.preprocessing.image import ImageDataGenerator
# from keras.callbacks import ReduceLROnPlateau

# Load data
trainDataSet = pandas.read_csv("train.csv")

phrases = trainDataSet["phrase"]
# print(text)
feeling = trainDataSet["emotion"]

for i in range(10):
  print(phrases[i])

vals = {}

for i in range(len(phrases)):
  words = phrases[i].split()
  for j in range(len(words)):
    if (words[j] in vals):
      vals[words[j]] += 1
    else:
      vals[words[j]] = 1

output = open("dict.txt", "w") # rename file to dict.csv
for i in vals:
  print(str(i) + "," + str(vals[i]), file = output)
output.close()