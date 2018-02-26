import os
import sys


# Code by James Martin, Emory University
# james.martin@emory.edu

class Search:

    def __init__(self, ext_1, ext_2):
        self.ext_1 = ext_1
        self.ext_2 = ext_2

    def dir_search(self):
        # searches directory for paths of files
        pass

    def confirm(self):
        # asks for user to confirm delete
        pass

    def to_trash(self):
        # sends junk data to trash
        pass


# reference code
# todo: delete this code after Search class is complete
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def test(ext_1, ext_2):
    search = Search(ext_1, ext_2)
    # search all directories for a search file name, or check flag for batch search
    # regardless of extension.
    # store paths in dictionary
    search.dir_search()
    # print confirmation to move to trash
    search.confirm()
    # move to trash
    search.to_trash()



    pass


if __name__ == "__main__":
    # check correct length args
    if len(sys.argv) == 1:
        print("No arguments passed, running default mode. Default arguments: [.doc .pdf]")
        test(".doc", ".pdf")
    elif len(sys.argv[1:]) == 2:
        print("Searching for given extensions")

    else:
        print("Invalid number of arguments passed. Please input: 'ext1 ext2 searchterms")
