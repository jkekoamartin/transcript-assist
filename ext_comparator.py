import csv
import os
import shutil
import sys
from pathlib import Path
import itertools


# Code by James Martin, Emory University
# james.martin@emory.edu 3/2/2018
# python 3.6


class Paths:

    def __init__(self):
        # dict that contains trash item name and its path {item:path} (same for rest)
        self.duplicates = {}
        # dict contains complete items and their path
        self.complete = {}
        # dict of incomplete items and their paths
        self.incomplete = {}


class Search:

    # by default, output path is the same directory that script is located in
    def __init__(self, s_ext_1, s_ext_2, s_search_paths, output_path=os.getcwd()):

        self.ext_1 = s_ext_1
        self.ext_2 = s_ext_2

        # this is now a list of paths
        self.search_paths = s_search_paths

        self.output_path = output_path

        self.result_paths = Paths()

        # read from file, delimited by newline (enter/return)

    def dir_search(self, ext):

        to_chain = []

        # return search results for given path
        for path in self.search_paths:
            glob_search = Path(path)
            search_files = glob_search.rglob('*' + ext)
            to_chain.append(search_files)

        # chain results together

        temp_result = to_chain.pop()

        # don't iterate on empty list
        if to_chain:
            for result in to_chain:
                temp_result = itertools.chain(temp_result, result)

        return temp_result

    def compare(self):
        """searches directory for search files. returns result object containing path to trash items (duplicates),
        complete items (ext_1, ext_2 pairs), and incomplete items (ext_1)"""

        # search result storage
        results_paths = self.result_paths
        to_search = []

        # for each search path, get results
        # this now is one list of all results from each search directory
        search_files = self.dir_search(self.ext_1)

        # drop ext, so we can compare with search for docs
        to_search_paths = []

        for item in search_files:
            p = Path(item)
            item = str(p.stem)
            if item in to_search:
                # don't add duplicate search terms
                continue
            else:
                to_search.append(item)
                to_search_paths.append(p)

        duplicates = {}
        complete = {}

        files = self.dir_search(self.ext_2)

        for file in files:
            p = Path(file)
            item = str(p.stem)
            if item in to_search and str(p.suffix).lower() != str(Path(self.ext_1)):
                # if already complete, then it is duplicate
                if file.name in complete:
                    duplicates[file.name] = file
                else:
                    complete[file.name] = file

        complete_list = []

        for file in complete:
            name = complete[file]
            complete_list.append(str(name.stem))

        incomplete = {}
        # we want to get incomplete ext1
        for file in to_search_paths:
            p = Path(file)
            item = str(p.stem)
            if item in complete_list:
                continue
            else:
                if p.name in incomplete:
                    continue
                else:
                    incomplete[p.name] = p

        results_paths.duplicates = duplicates
        results_paths.complete = complete
        # remove from search if complete, so to_search contains incomplete files
        results_paths.incomplete = incomplete

    def to_csv(self):

        paths = [(Path(self.output_path).joinpath('complete.csv'), self.result_paths.complete),
                 (Path(self.output_path).joinpath('incomplete.csv'), self.result_paths.incomplete),
                 (Path(self.output_path).joinpath('duplicates.csv'), self.result_paths.duplicates)
                 ]

        for path, files in paths:

            with open(path.absolute(), 'w', newline='') as csvfile:
                fieldnames = ['File_Name', 'Path_To_File']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for file in files:
                    writer.writerow({'File_Name': file, 'Path_To_File': files[file]})

    def confirm(self):
        # asks for user to confirm delete

        command = input("Would you like to copy the search results to the output folder? (y/n)")

        if command is "y":
            pass
        elif command is "n":
            print("Okay, no changes have been made. You can check output.csv to see what files were duplicates. "
                      "Exiting program")
            sys.exit()
        else:
            print("Please input 'y' or 'n'")
            self.confirm()

        print("Check the outputs 'complete.csv' and 'incomplete.csv' to see which " + str(self.ext_1) + "s have " +
                  str(self.ext_2)
                  + " "
                    "matches! They are stored in the directory being searched so that they don't get lost!")
        print()
        print("***Important*** The outputs 'complete.csv' and 'incomplete.csv' are overwritten each time the "
                  "program is run.")
        print("This prevents clutter, but to keep snapshots of the results, just move them out of the directory "
                  "they are in. This will prevent the program from overwriting them with new ones!")

    def move(self, output=None):
        if output is None:
            p = Path(self.search_paths).absolute()
            p2 = Path(*p.parts[:len(p.parts) - 1]).joinpath("ext_comparator_OUTPUT")
            if p2.exists():
                pass
            else:
                p2.mkdir(True, True)
        else:
            p = Path(output).absolute()
            p2 = Path(*p.parts[:len(p.parts) - 1]).joinpath("OUTPUT")

        result_paths = self.result_paths


        # this copies the duplicates into a duplicate folder in output
        for each in result_paths.duplicates:
            f = Path(result_paths.duplicates[each]).absolute()

            # print(trash_items.trash[each])
            if f.exists():
                p2.joinpath("duplicate")
                shutil.copy(str(f), str(p2))
            else:
                shutil.copy(str(f), str(p))
        print("Files moved to duplicates folder in output (trash folder just outside working directory).")


# this runs default program arguments
def run_default(in_ext_1, in_ext_2, in_search_path):
    in_search = Search(in_ext_1, in_ext_2, in_search_path)
    # search all directories for a search file name, or check flag for batch search
    # regardless of extension.
    # store paths in dictionary
    in_search.compare()
    # write to csvs

    in_search.to_csv()

    # print confirmation to move to trash
    in_search.confirm()
    # move to trash
    in_search.move()


if __name__ == "__main__":
    # check correct length args

    if len(sys.argv) == 1:
        print("No arguments passed, running default mode. Default arguments: [.pdf .doc* CurrentDirectoryPath]")
        cwd = os.getcwd()
        # note: script accepts multiple search paths, so even single a search path is are passed in an array
        run_default('.pdf', '.*', ["C:/Users/James/Documents/transcripts", "C:/Users/James/Documents/transcripts1"])

    elif len(sys.argv[1:]) == 3:
        ext_1, ext_2, search_path = sys.argv[1:]
        print("Searching for " + ext_1 + ", " + ext_2 + " pairs" + "in " + search_path)
        run_default(str(ext_1), str(ext_2), [search_path])

    elif len(sys.argv[1:]) == 2:
        cwd = os.getcwd()
        ext_1, ext_2 = sys.argv[1:]
        print("Searching for " + ext_1 + ", " + ext_2 + " pairs" + "in " + cwd)
        run_default(str(ext_1), str(ext_2), [cwd])

    # this is a run mode for two search directories. The code can take any mount of search paths, but it would be messy
    # to pass in more than two path via terminal
    elif len(sys.argv[1:]) == 4:
        ext_1, ext_2, search_path_1, search_path_2 = sys.argv[1:]
        print("Searching for " + ext_1 + ", " + ext_2 + " pairs" + "in " + search_path_1 + " and " + search_path_2)

        search_paths = [search_path_1, search_path_2]

        run_default(str(ext_1), str(ext_2), search_paths)

    else:
        print("Invalid number of arguments passed. Please input: 'ext1 ext2 searchdirectory', or run with out "
              "argument for default program parameters: [.pdf .docx CurrentDirectoryPath]")
