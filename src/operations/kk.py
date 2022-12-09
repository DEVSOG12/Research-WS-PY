# # Compile all Organization Names into a list from ./data/ChildrensRights.csv files
import csv
# import os
# import shutil
#
#
def get_org_names():
    org_names = []
    with open("../../data/MentalHealthAddictionRecovery.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            org_names.append(row[0])
    print(org_names)
    org_names.remove('Organization Name')
    org_names = list(set(org_names))
    # Remove Empty Strings
    org_names = [x for x in org_names if x]
    # Replace each space with a dash
    org_names = [x.replace(" ", "_") for x in org_names]
    return org_names
#
#
# # Check if a string does not contain any element in a list
def containsNone(strr, listk):
    return any([x in strr for x in listk])
#

# # Function that goes through a folder ./x and removes folder that are not in the list of org_names
#
#
# # remove_folders(get_org_names())
#
#
# # Function that copies files from ../../liwc/ to ../../liwcCorrected/ that have folders that are already in ../../liwcCorrected/
# # def copy_files():
# #     for root, dirs, files in os.walk("../../liwc"):
# #         for file in files:
# #             if file.endswith(".txt"):
# #                 # Check if the folders exist and create them if they don't
# #                 if not os.path.exists("../../liwcCorrected/" + root[10:]):
# #                     os.makedirs("../../liwcCorrected/" + root[10:])
# #                 # Copy the file to the new folder
# #
# #                 shutil.copy(os.path.join(root, file), "../../liwcCorrected/" + root[10:] + "/" + file)
# #                 # shutil.copy(os.path.join(root, file), os.path.join("./liwc", root[9:]))
# #                 print("Copied " + file + " to " + os.path.join("../../liwcCorrected", root[10:]))
# #
# #
# #
# #
# # copy_files()
#
# # Function that goes gets a folder ../../liwcCorrected/TortureCombatantsPrisonersTerror.csv and removes folders that
# # are not in the list of org_names and still retains the content of the folder that are in org_names
# def remove_folders(org_names):
#     for root, dirs, files in os.walk("../../liwcK/HumanTrafficking.csv"):
#         for dir in dirs:
#             if dir not in org_names and containsNone(str(os.path.join(root, dir)), org_names):
#                 print("Removing " + dir)
#                 shutil.rmtree(os.path.join(root, dir))
#
#     # Check if the len(org_names) == len(folders) in the  folder. ./../liwcCorrected/CriminalJustice.csv
#     if len(org_names) == len(os.listdir("../../liwcK/HumanTrafficking.csv")):
#         print("All folders are present")
#
#
# remove_folders(get_org_names())
import os
import shutil
from typing import Optional, List


# Write an API that generates fancy sequences using the append, addAll, and multAll operations.
#
# Implement the Fancy class:
#
# Fancy() Initializes the object with an empty sequence.
# void append(val) Appends an integer val to the end of the sequence.
# void addAll(inc) Increments all existing values in the sequence by an integer inc.
# void multAll(m) Multiplies all existing values in the sequence by an integer m.
# int getIndex(idx) Gets the current value at index idx (0-indexed) of the sequence modulo 109 + 7. If the index is greater or equal than the length of the sequence, return -1.


# Function that goes gets a folder ../../liwcCorrected/TortureCombatantsPrisonersTerror.csv and removes folders that


# are not in the list of org_names and still retains the content of the folder that are in org_names
def remove_folders(org_names):
    for root, dirs, files in os.walk("../../liwcK/TortureCombatantsPrisonersTerror.csv"):
        for dir in dirs:
            if dir not in org_names and not containsNone(str(os.path.join(root, dir)), org_names):
                print("Removing " + str(os.path.join(root, dir)),)
                shutil.rmtree(os.path.join(root, dir))

    # Check if the len(org_names) == len(folders) in the  folder. ./../liwcCorrected/CriminalJustice.csv
    # if len(org_names) == len(os.listdir("../../liwcK/ChildrensRights.csv")):
    #     print("All folders are present")

# remove_folders(get_org_names())

# Check if the len(org_names) == len(folders) in the  folder. ./../liwcCorrected/CriminalJustice.csv
def check_folders(org_names):
    if len(list(set(org_names))) == len(os.listdir("../../liwcK/MentalHealthAddictionRecovery.csv")):
        print("All folders are present")
    else:
        print("Not all folders are present")
        print("Number of folders in the folder: " + str(len(os.listdir("../../liwcK/MentalHealthAddictionRecovery.csv"))))
        print("Number of folders in the list: " + str(len(list(set(org_names)))))
# if len(org_names) == len(os.listdir("../../liwcK/ChildrensRights.csv")):
#     print("All folders are present")

check_folders(get_org_names())