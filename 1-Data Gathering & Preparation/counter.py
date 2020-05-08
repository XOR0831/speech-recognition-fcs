import re
import os

path = "./Data_Clean/"
pattern = "^UNKNOWN*"

print("STARTED")
for volume in os.listdir(path):
  unknown = 0
  single_word = 0
  multiple_word = 0
  total = 0
  for folder in os.listdir(path + volume):
    for file in os.listdir(path + volume + "/" + folder):
      for word in os.listdir(path + volume + "/" + folder + "/" + file):
        total += 1
        words = str(word[:-4]).split()
        if len(words) == 1:
          if re.match(pattern, words[0]) != None:
            unknown += 1
          else:
            single_word += 1
        else:
          if words[1].isdigit():
            single_word += 1
          else:
            multiple_word += 1
  print(volume)
  print("Unknown words: " + str(unknown))
  print("Single words: " + str(single_word))
  print("Multiple words: " + str(multiple_word))
  print("Total words: " + str(total))
print("ENDED")
