import math
import random
import os
import sys

samples = 1700


def reservoir_sampling():
    reservoir = []
    count = 0
    for root, directories, files in os.walk(sys.argv[1]):
        for file in files:
            if '.txt' in file:
                if count < samples:
                    reservoir.append(os.path.join(root, file))
                else:
                    i = random.randint(0, count)
                    if i < samples:
                        reservoir[i] = os.path.join(root, file)
                count += 1

    return reservoir


test_sample = reservoir_sampling()
no_of_spam_files = 0
no_of_ham_files = 0
spam_file_paths = []
ham_file_paths = []
total_words = 0

for file_name in test_sample:
    if file_name.__contains__(".ham."):
        ham_file_paths.append(file_name)
        no_of_ham_files += 1
    if file_name.__contains__(".spam."):
        spam_file_paths.append(file_name)
        no_of_spam_files += 1


prob_spam = no_of_spam_files / (no_of_spam_files + no_of_ham_files)
print(prob_spam)

prob_ham = no_of_ham_files / (no_of_spam_files + no_of_ham_files)
print(prob_ham)

unique_word_count = 0
word_count_spam = dict()
word_count_ham = dict()

for file in spam_file_paths:
    file_pointer = open(file, "r", encoding="latin1")
    contents = file_pointer.read()
    for word in contents.split():
        word = word.lower()
        total_words = total_words + 1
        if word not in word_count_spam:
            unique_word_count += 1
        word_count_spam[word] = 1 if word_count_spam.get(word) is None \
            else word_count_spam.get(word.lower()) + 1

total_words_spam = total_words
total_words = 0

for file in ham_file_paths:
    file_pointer = open(file, "r", encoding="latin1")
    contents = file_pointer.read()
    for word in contents.split():
        word = word.lower()
        total_words = total_words + 1
        if word not in word_count_ham and word not in word_count_spam:
            unique_word_count += 1
        word_count_ham[word] = 1 if word_count_ham.get(word) is None \
            else word_count_ham.get(word.lower()) + 1

total_words_ham = total_words

file_pointer_model = open("nbmodel_sample.txt", "w", encoding="latin1")

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