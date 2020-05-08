import re
import os
import shutil
import datetime

path = "./Data_Clean/"
pattern = "^unknown*"
path_sorted = "./Data_Sorted/"
single_words = []
words_folder = os.listdir(path_sorted)
if not "PHRASES" in words_folder:
    os.makedirs(path_sorted + "PHRASES")
print("STARTED")
for volume in os.listdir(path):
  for folder in os.listdir(path + volume):
    for file in os.listdir(path + volume + "/" + folder):
      for word in os.listdir(path + volume + "/" + folder + "/" + file):
        words = str(word[:-4].lower()).split()
        if len(words) == 1:
          if not words[0] in words_folder:
            os.makedirs(path_sorted + str(words[0]))
            words_folder.append(words[0])
          
          if re.match(pattern, words[0]) != None:
            # shutil.move(path + volume + "/" + folder + "/" + file + "/" + word, path_sorted + "UNKNOWN" + "/" + words[0] + "/" + word)
            print(word + "->" + path_sorted + "UNKNOWN")
          else:
            if words[0] in single_words:
              shutil.move(path + volume + "/" + folder + "/" + file + "/" + word, path_sorted + str(words[0]) + "/" + str(words[0]) + " " + str(datetime.datetime.now().second) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().hour) + ".wav")
              print(word + "->" + path_sorted + str(words[0]) + "*")
            else:
              shutil.move(path + volume + "/" + folder + "/" + file + "/" + word, path_sorted + str(words[0]) + "/" + word)
              single_words.append(words[0])
              print(word + "->" + path_sorted + str(words[0]))
        else:
          if words[1].isdigit():
            if not words[0] in words_folder:
              os.makedirs(path_sorted + str(words[0]))
              words_folder.append(words[0])
            shutil.move(path + volume + "/" + folder + "/" + file + "/" + word, path_sorted + str(words[0]) + "/" + word)
            print(word + "->" + path_sorted + str(words[0]))
          else:
            shutil.move(path + volume + "/" + folder + "/" + file + "/" + word, path_sorted + "PHRASES" + "/" + word)
            print(word + "->" + path_sorted + "PHRASES")
  print(volume)
print("Total Words: " + str(len(words_folder)))
print("ENDED")
