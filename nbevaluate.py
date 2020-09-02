import sys

outputFile = open(sys.argv[1].rstrip(), "r", encoding="latin1")

line = outputFile.readline().rstrip()

true_positive_spam = 0
false_positive_spam = 0
true_negative_spam = 0
false_negative_spam = 0

true_positive_ham = 0
false_positive_ham = 0
true_negative_ham = 0
false_negative_ham = 0

while line:
    split_string = line.lower().split()

    if split_string[1].__contains__(".ham.") and split_string[0].__eq__("ham"):
        true_positive_ham += 1
    elif split_string[1].__contains__(".ham.") and split_string[0].__eq__("spam"):
        false_negative_ham += 1
        false_positive_spam += 1
    elif split_string[1].__contains__(".spam.") and split_string[0].__eq__("spam"):
        true_positive_spam += 1
    elif split_string[1].__contains__("spam") and split_string[0].__eq__("ham"):
        false_negative_spam += 1
        false_positive_ham += 1

    line = outputFile.readline()

print("TP_Spam " + str(true_positive_spam))
print("FP_Spam " + str(false_positive_spam))
print("FN Spam " + str(false_negative_spam))

print("TP_Ham " + str(true_positive_ham))
print("FP_Ham " + str(false_positive_ham))
print("FN Ham " + str(false_negative_ham))


precision_spam = true_positive_spam / (true_positive_spam + false_positive_spam)
recall_spam = true_positive_spam / (true_positive_spam + false_negative_spam)
f1_spam = 2 * precision_spam * recall_spam / (precision_spam + recall_spam)

precision_ham = true_positive_ham / (true_positive_ham + false_positive_ham)
recall_ham = true_positive_ham / (true_positive_ham + false_negative_ham)
f1_ham = 2 * precision_ham * recall_ham / (precision_ham + recall_ham)

print(precision_spam)
print(recall_spam)
print(f1_spam)

print(precision_ham)
print(recall_ham)
print(f1_ham)