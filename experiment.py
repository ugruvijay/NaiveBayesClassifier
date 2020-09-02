import os
import sys
import math
import time

import nltk
from nltk.stem import PorterStemmer
import string
from nltk.corpus import stopwords

nltk.download('stopwords')
ps = PorterStemmer()
start_time = time.time()

stop_words = set(stopwords.words('english'))

spam_files_paths = []
ham_files_paths = []
word_count_spam = dict()
word_count_ham = dict()
no_of_spam_files = 0
no_of_ham_files = 0

for root, directories, files in os.walk(sys.argv[1]):
    for file in files:
        if '.txt' in file:
            directory_name, file_name = os.path.split(os.path.join(root, file))
            parent_directory = directory_name.split('/')
            parent_directory = parent_directory[len(parent_directory) - 1]
            if parent_directory == "spam":
                no_of_spam_files += 1
                spam_files_paths.append(os.path.join(root, file))
            elif parent_directory == "ham":
                no_of_ham_files += 1
                ham_files_paths.append(os.path.join(root, file))

total_words = 0

print(str(no_of_ham_files + no_of_spam_files))

prob_spam = no_of_spam_files / (no_of_spam_files + no_of_ham_files)
print(prob_spam)

prob_ham = no_of_ham_files / (no_of_spam_files + no_of_ham_files)
print(prob_ham)

unique_word_count = 0

for file in spam_files_paths:
    file_pointer = open(file, "r", encoding="latin1")
    contents = file_pointer.read()
    for word in contents.split():
        word = word.lower()
        if word not in string.punctuation and word not in stop_words:
            word = ps.stem(word)
            total_words = total_words + 1
            if word not in word_count_spam:
                unique_word_count += 1
            word_count_spam[word] = 1 if word_count_spam.get(word) is None \
                else word_count_spam.get(word.lower()) + 1

total_words_spam = total_words
total_words = 0

for file in ham_files_paths:
    file_pointer = open(file, "r", encoding="latin1")
    contents = file_pointer.read()
    for word in contents.split():
        word = word.lower()
        if word not in string.punctuation and word not in stop_words:
            word = ps.stem(word)
            total_words = total_words + 1
            if word not in word_count_ham and word not in word_count_spam:
                unique_word_count += 1
            word_count_ham[word] = 1 if word_count_ham.get(word) is None \
                else word_count_ham.get(word.lower()) + 1

total_words_ham = total_words

file_pointer_model = open("nbmodel.txt", "w", encoding="latin1")

file_pointer_model.write(str(math.log(prob_spam)) + "\n")
file_pointer_model.write(str(math.log(prob_ham)) + "\n")
file_pointer_model.write(str(unique_word_count) + "\n")
file_pointer_model.write(str(total_words_spam) + "\n")
file_pointer_model.write(str(total_words_ham) + "\n")

for word in word_count_spam:
    file_pointer_model.write("spam " + word + " " +
                             str(math.log((word_count_spam[word] + 1)/(total_words_spam + unique_word_count))) + "\n")

for word in word_count_ham:
    file_pointer_model.write("ham " + word + " " +
                             str(math.log((word_count_ham[word] + 1) / (total_words_ham + unique_word_count))) + "\n")

file_pointer_model.close()

print(str(time.time() - start_time))
