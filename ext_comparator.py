import csv
import os
import shutil
import sys
from pathlib import Path


# Code by James Martin, Emory University
# james.martin@emory.edu


class Paths:

    def __init__(self):
        # dict that contains trash item name and its path
        self.trash = {}
        # dict contains complete items and their path
        self.complete = {}
        # dict of incomplete items
        self.incomplete = []


class Search:

    def __init__(self, s_ext_1, s_ext_2, s_search_path):
        self.search_path = s_search_path
        self.ext_1 = s_ext_1
        self.ext_2 = s_ext_2

        self.paths = Paths()

        # read from file, delimited by newline (enter/return)

    # todo: implement class functions
    def dir_search(self):
        """searches directory for search files. returns result object containing path to trash items (duplicates),
        complete items (ext_1, ext_2 pairs), and incomplete items (ext_1)"""

        search_paths = self.paths
        to_search = []

        # replace ext_1 with ext_2 for search, sanitizes irregular case .ext
        glob_search = Path(self.search_path)
        search_files = glob_search.rglob('*' + self.ext_1)

        for item in search_files:
            p = Path(item)
            item = str(p.stem) + self.ext_2
            if item in to_search:
                # don't add duplicate search terms
                continue
            else:
                to_search.append(item)

        trash = {}
        complete = {}

        files = glob_search.rglob('*' + self.ext_2)

        for file in files:
            string = str(file.name)
            if string in to_search:
                # if already complete, then it is duplicate
                if file.name in complete:
                    trash[file.name] = file
                else:
                    complete[file.name] = file

        # check completion
        for item in complete:
            string = str(item)
            to_search.remove(string)

        search_paths.trash = trash
        search_paths.complete = complete
        # remove from search if complete, so to_search contains incomplete files
        search_paths.incomplete = to_search

    def confirm(self):
        # asks for user to confirm delete
        search_items = self.paths

        path = Path(self.search_path).joinpath('complete.csv')

        with open(path.absolute(), 'w', newline='') as csvfile:
            fieldnames = ['File_Name', 'Path_To_File']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for complete in self.paths.complete:
                writer.writerow({'File_Name': complete, 'Path_To_File': self.paths.complete[complete]})

        path = Path(self.search_path).joinpath('incomplete.csv')
        with open(path.absolute(), 'w', newline='') as csvfile:
            fieldnames = ['File_Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for incomplete in self.paths.incomplete:
                incomplete = str(Path(incomplete).stem) + self.ext_1

                writer.writerow({'File_Name': incomplete})

        path = Path(self.search_path).joinpath('duplicates.csv')
        with open(path.absolute(), 'w', newline='') as csvfile:
            fieldnames = ['File_Name', 'Path_To_File']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for trash in self.paths.trash:
                writer.writerow({'File_Name': trash, 'Path_To_File': self.paths.trash[trash]})

        if search_items.trash:
            for item in search_items.trash:
                path = search_items.trash[item]
                print("File: " + item + " Location: " + str(path))

            command = input("Would you like to move these duplicate items to junk file (in search directory)? (y/n)")

            if command is "y":
                pass
            elif command is "n":
                print("Okay, no changes have been made. You can check output.csv to see what files were duplicates. "
                      "Exiting program")
                sys.exit()
            else:
                print("Please input 'y' or 'n'")
                self.confirm()
        else:
            print("No duplicates found!")
            print("Check the outputs 'complete.csv' and 'incomplete.csv' to see which " + str(self.ext_1) + "s have " +
                  str(self.ext_2)
                  + " "
                    "matches! They are stored in the directory being searched so that they don't get lost!")
            print()
            print("***Important*** The outputs 'complete.csv' and 'incomplete.csv' are overwritten each time the "
                  "program is run.")
            print("This prevents clutter, but to keep snapshots of the results, just move them out of the directory "
                  "they are in. This will prevent the program from overwriting them with new ones!")

    def to_trash(self):
        trash_items = self.paths
        p = Path(self.search_path).absolute()
        p = Path(*p.parts[:len(p.parts) - 1]).joinpath("trash")
        if p.exists():
            pass
        else:
            p.mkdir(True, True)

        for each in trash_items.trash:
            f = Path(trash_items.trash[each]).absolute()

            # print(trash_items.trash[each])
            if f.exists():
                f.joinpath("dupedagain")
                shutil.move(str(f), str(p))
            else:
                shutil.move(str(f), str(p))
        print("Files moved to trash (trash folder just outside working directory).")


# this runs default program arguments
# todo: implement run mode with option flags
def run_default(in_ext_1, in_ext_2, in_search_path):
    in_search = Search(in_ext_1, in_ext_2, in_search_path)
    # search all directories for a search file name, or check flag for batch search
    # regardless of extension.
    # store paths in dictionary
    in_search.dir_search()
    # print confirmation to move to trash
    in_search.confirm()
    # move to trash
    in_search.to_trash()


if __name__ == "__main__":
    # check correct length args
    if len(sys.argv) == 1:
        print("No arguments passed, running default mode. Default arguments: [.pdf .docx CurrentDirectoryPath]")
        cwd = os.getcwd()
        run_default(".pdf", ".docx", cwd)

    elif len(sys.argv[1:]) == 3:
        ext_1, ext_2, search_path = sys.argv[1:]
        print("Searching for " + ext_1 + "," + ext_2 + " pairs" + "in " + search_path)
        run_default(ext_1, ext_2, search_path)

    elif len(sys.argv[1:]) == 2:
        cwd = os.getcwd()
        ext_1, ext_2 = sys.argv[1:]
        print("Searching for " + ext_1 + "," + ext_2 + " pairs" + "in " + cwd)
        run_default(ext_1, ext_2, cwd)

    else:
        print("Invalid number of arguments passed. Please input: 'ext1 ext2 searchdirectory', or run with out "
              "argumentd for default program parameters: [.pdf .docx CurrentDirectoryPath]")
