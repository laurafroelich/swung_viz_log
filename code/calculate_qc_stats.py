import lasio
import os

def count_number_of_particular_files(directory, extension):
    """
    Count number of files in directory (including all subdirectories) of file type extension.

    :param directory: path to folder in which files of certain type need to be counted.
    :param extension: extension for which to count number of files.
    :return: number of files of type extension in directory.
    """

    count = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.split('.')[-1] == extension:
                count = count+1

    return count

def count_number_of_files(directory):
    """
    Count number of files in directory (including all subdirectories) of file type extension.

    :param directory: path to folder in which files of certain type need to be counted.
    :return: number of files in directory.
    """

    count = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
                count = count+1

    return count

