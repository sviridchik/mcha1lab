import math as m

raw_data = input("Enter please the text :  ").strip(".,!?:;").lower().split(".")
print(raw_data)
data = []
raw_data_processed = ""
for sentence in raw_data:
    sentence = sentence.replace(",", "")
    data.append(sentence.split())
    raw_data_processed+=("".join(sentence)).replace(" ", "")
print(data)

print(raw_data_processed)


def first_task(data: list, raw_data_processed: str, k=10, n=4) -> None:
    """ 1)fruquince of every word
        2)average amount of words in a sentence
        3)median
        4)top k most frequince n words
    """
    amount = 0
    d1 = dict()
    for sentence in data:
        for word in sentence:
            amount += 1
            if word in d1:
                d1[word] += 1
            else:
                d1[word] = 1
    for kk, v in d1.items():
        pass
        print("Word '{0}'  occurs {1}  times".format(kk, v))
    print("Average amount of words in a sentence is {}".format(amount/len(data)))
    lens = []
    for sentence in data:
        lens.append(len(sentence))
    lens.sort()
    # lens = [1, 3, 5, 7]
    l = len(lens)
    if l % 2 != 0 and l != 1:
        print("median is {}".format(lens[(1 + len(lens)) // 2]))
    elif l == 1:
        print("median is {}".format(lens[0]))
    else:
        res = (1 + len(lens)) / 2 - 1
        print("median is {}".format((lens[m.trunc(res)] + lens[m.ceil(res)]) // 2))

    command = input("Do you want to enter k and v (y/n)")
    if command == "y":
        k = int(input("Enter please k : "))
        v = int(input("Enter please v : "))
    elif command == "n":
        print("All right")
    else:
        print("Unknown command")

        # 4
    s = raw_data_processed
    # s = "abcabdabcabc"
    # n = 3
    # k = 3
    d4 = {}
    for i in range(len(s) - 2):
        etalon = s[i:i + n]
        if etalon in d4:
            continue
        for j in range(len(s) - (n - 1)):
            word = s[j:j + n]
            if word == etalon:
                if word in d4:
                    d4[word] += 1
                else:
                    d4[word] = 1

    tmp_list = list(d4.items())
    tmp_list.sort(key=lambda node: node[1], reverse=True)
    tmp_list = tmp_list[0:k]
    print(tmp_list)
    for item in tmp_list:
        # pass
        print("Word '{0}'  occurs {1}  times".format(item[0], item[1]))


first_task(data, raw_data_processed)

# check
# https://planetcalc.ru/3205/
