import os
import shutil
import sys
import pathlib
import re
import fnmatch


# Code by James Martin, Emory University
# james.martin@emory.edu


class Paths:

    def __init__(self):
        # dict that contains trash item name and its path
        self.trash = {}
        #
        self.complete = {}
        # dict of incomplete items and their path
        self.incomplete = {}


class Search:

    def __init__(self, ext_1, ext_2, search, search_path):
        self.search_path = search_path
        self.search = search
        self.ext_1 = ext_1
        self.ext_2 = ext_2

        self.paths = Paths()

        # read from file, delimited by newline (enter/return)
        search_terms = open(search).read().splitlines()

        self.search_terms = search_terms

    # todo: implement class functions
    def dir_search(self):
        """searches directory for search files. returns result object containing path to trash items (duplicates),
        complete items (ext_1, ext_2 pairs), and incomplete items (ext_1)"""

        search_paths = self.paths
        to_search = []

        # replace ext_1 with ext_2 for search
        for item in self.search_terms:
            item = item.replace(self.ext_1, self.ext_2)
            to_search.append(item)

        trash = search_paths.trash
        complete = search_paths.complete
        incomplete = search_paths.incomplete

        files = find_all()

        while to_search:
            temp = to_search.pop()

            for search_term in search_results:
                print("LOL")
                print(search_term)

                # if search_term not in completed:
                #     completed[search_term] = 1
                # else:
                #     completed[search_term] += 1

    def confirm(self):
        # asks for user to confirm delete
        search_items = self.paths

        for item, path in search_items.trash:
            print("File: " + item + " Location: " + path)

        command = input("Would you like to move these duplicate items to trash? (y/n)")

        if command is "y":
            self.to_trash()
        elif command is "n":
            print("Okay, no changes have been made. Exiting program")
            sys.exit()

    def to_trash(self):
        trash_items = self.paths

        shutil.move()
        # sends junk data to trash
        pass


# reference code
# todo: delete what is not needed
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def find_all(name, path):

    for x in path.rglob('*' + self.ext_1):


cwd = os.getcwd()


# this runs default program arguments
# todo: implement run mode with option flags
def run_default(ext_1, ext_2, search, search_path):
    search = Search(ext_1, ext_2, search, search_path)
    # search all directories for a search file name, or check flag for batch search
    # regardless of extension.
    # store paths in dictionary
    search.dir_search()
    # print confirmation to move to trash
    search.confirm()
    # move to trash
    search.to_trash()


if __name__ == "__main__":
    # check correct length args
    if len(sys.argv) == 1:
        print("No arguments passed, running default mode. Default arguments: [.pdf .docx search.txt]")
        run_default(".pdf", ".doc*", "search.txt", "C:/Users/James/Documents/transcripts")
    elif len(sys.argv[1:]) == 2:
        print("Searching for given extensions")

    else:
        print("Invalid number of arguments passed. Please input: 'ext1 ext2 searchterms")
