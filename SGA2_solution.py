import re
import json
import argparse
from collections import defaultdict


class InvertedIndex:
    def __init__(self, data):
        self.data = data

    def query(self, words):
        for word in words:
            if not self.data.get(word):  # checking a word in the dictionary
                return set()  # return an empty set
        return set.intersection(
            *[self.data[word] for word in words]
        )  # set of article_id for all words

    def dump(self, filepath):
        with open(filepath, "w") as file:  # open file
            file.write(
                json.dumps(
                    {
                        word: tuple(articles_id)
                        for word, articles_id in self.data.items()
                    }
                )
            )  # writing data to disk using json {word: tuple(articles_id)}

    @classmethod
    def load(cls, filepath):
        with open(filepath, "r") as file:  # open file
            return InvertedIndex(
                {
                    word: set(articles_id)
                    for word, articles_id in json.load(file).items()
                }
            )  # load data from disk {word: set(articles_id)}


def load_document(filepath):
    result_dict = {}  # create empty dict
    with open(filepath, "r", encoding="utf8") as file:  # open file
        for string in file:
            data = re.match(
                r"([0-9]+)(.*)", string
            ).groups()  # search ([0-9]+) = article_id, (.*) = the text
            result_dict[int(data[0])] = data[1].strip()  # add data in dict
    return result_dict  # {article_id: article_content}


def build_inverted_index(articles):
    result_dict = defaultdict(set)  # create empty defaultdict(set)
    for index, string in articles.items():
        for word in string.split():
            result_dict[word].add(index)  # add data {word: set(articles_id)}
    return InvertedIndex(result_dict)  # InvertedIndex object


parser = argparse.ArgumentParser()  # create object "parser"
parser.add_argument("command", type=str)  # add argument "command", type = str
parser.add_argument(
    "--dataset",
    type=str,
    default="data/wikipedia_sample.txt",
    help="path to dataset to build Inverted Index",
)  # add optional argument "--dataset", type = str
parser.add_argument(
    "--index",
    type=str,
    default="index/index.json",
    help="path for Inverted Index dump OR path to load Inverted Index",
)  # add optional argument "--index", type = str
parser.add_argument(
    "--query_file",
    type=str,
    help="(query_file with collection of queries to run against InvertedIndex",
)  # add optional argument "--query_file", type = str

args = parser.parse_args()  # passing arguments to the variable "args"
if args.command == "build" and args.dataset and args.index:
    inverted_index = build_inverted_index(
        load_document(args.dataset)
    )  # load document data and build InvertedIndex object
    inverted_index.dump(
        args.index
    )  # writing data to disk using json format {word: tuple(articles_id)}

elif args.command == "query" and args.index and args.query_file:
    result = []  # creating an empty list
    inverted_index = InvertedIndex.load(
        args.index
    )  # load data from disk {word: set(articles_id)}
    with open(args.query_file, "r") as file:  # open file
        for words in file:
            result.append(
                sorted(inverted_index.query(words.split()))
            )  # choose common articles for all words in the query, add in list
    for sublist in result:
        print(",".join(str(number) for number in sublist))  # print articles id

# Comments why my solution is unusual:
# 1. Implemented a short and clear code;
# 2. A fairly high-performance code has been implemented.
#    For the wikipedia file specified in the task,
#    the inverted index is created in 6.60 seconds
#    (build_inverted_index(load_document(filepath)));
# 3. Standard libraries are used - re, collections.
# 4. The average test time per test = 4.90 sec.

# P.S. Checker.py works if you enter "python" instead of "python3"
#      when using console commands. Time to run checker.py = 40.40 sec.
#      (the tests were carried out on the i7 6700k processor).
# P.S.S. Based on the conditions of the task, this program does not
#        work correctly. It would be better if, when processing text,
#        we excluded all characters except letters and numbers from
#        it and reduced them to a common case, since the current version
#        of the program considers "Python", "python" and "Python:=" to be
#        different words and does not look for a match for them. This
#        problem is easily solved using regular expressions.
