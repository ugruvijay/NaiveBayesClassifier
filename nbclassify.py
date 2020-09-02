import os
import sys
import time
import math

start_time = time.time()

model_dict = dict()

model = open("nbmodel.txt", "r", encoding="latin1")

prior_prob_spam = float(model.readline().rstrip())
prior_prob_ham = float(model.readline().rstrip())
no_unique_words = int(model.readline().rstrip())
no_spam_words = int(model.readline().rstrip())
no_ham_words = int(model.readline().rstrip())
line = model.readline().rstrip()
cnt = 1
while line:
    split_string = line.split()
    model_dict[split_string[0] + split_string[1]] = float(line.split()[2])
    line = model.readline()

output = open("nboutput.txt", "w")

correct_classification_spam = 0
correct_classification_ham = 0

for root, directories, files in os.walk(sys.argv[1]):
    for file in files:
        if '.txt' in file:
            directory_name, file_name = os.path.split(os.path.join(root, file))
            parent_directory = directory_name.split('/')
            parent_directory = parent_directory[len(parent_directory) - 1]

            prob_spam = prior_prob_spam
            prob_ham = prior_prob_ham
            file_pointer = open(os.path.join(root, file), "r", encoding="latin1")
            content = file_pointer.read()
            for word in content.split():
                lowercase_word = word.lower()
                if "spam" + lowercase_word in model_dict or "ham" + lowercase_word in model_dict:
                    if "spam" + lowercase_word in model_dict:
                        prob_spam = prob_spam + model_dict.get("spam" + lowercase_word)
                    else:
                        prob_spam = prob_spam + math.log(1 / (no_spam_words + no_unique_words))
                    if "ham" + lowercase_word in model_dict:
                        prob_ham = prob_ham + model_dict.get("ham" + lowercase_word)
                    else:
                        prob_ham = prob_ham + math.log(1 / (no_ham_words + no_unique_words))

            # prob_spam = prob_spam + prior_prob_spam
            # prob_ham = prob_ham + prior_prob_ham

            if prob_spam > prob_ham:
                if parent_directory == "spam":
                    correct_classification_spam += 1
                output.write("spam\t" + os.path.join(root, file) + "\n")
            elif prob_spam < prob_ham:
                if parent_directory == "ham":
                    correct_classification_ham += 1
                output.write("ham\t" + os.path.join(root, file) + "\n")
            else:
                print("Equal")

print(correct_classification_spam)
print(correct_classification_ham)

print(str(time.time() - start_time))
