# data_compare.py
# -*- coding: utf-8 -*-
# @Author: Sidharth Mishra
# @Date:   2017-05-15 11:50:38
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-05-15 11:51:44


"""
Script to compare the data generated by the pymining seqmining module and our
c++ port
"""

# pystdlib imports ~
from pprint import pprint
from re import findall
from re import compile
from argparse import ArgumentParser
from sys import exit

FILE_CPP = None
FILE_PYMINING = None

if __name__ == "__main__":
  """
  Compares the 2 files and checks if the outputs match, index -- freq mapping
  and the number of elements
  """

  parser = ArgumentParser()
  parser.add_argument("-fcpp", "--file-cpp")
  parser.add_argument("-fpy", "--file-pymining")

  parsed_args = parser.parse_args()

  FILE_CPP, FILE_PYMINING = parsed_args.file_cpp, parsed_args.file_pymining

  if FILE_CPP is None or FILE_PYMINING is None:
    parser.print_usage()
    exit(0)

  cpp_dict = dict()
  pymining_dict = dict()

  with open(FILE_CPP, 'r') as cpp_file:
    for line in cpp_file:
      # line looks like [[0 ]] 29037
      pattern = compile(r"\[\[(.*)\]\]\s{1}(\d*)")
      elements = findall(pattern, line)
      cpp_dict[elements[0][0].strip()] = elements[0][1]

  with open(FILE_PYMINING, "r") as pymining_file:
    for line in pymining_file:
      # line looks like (256) 21474
      pattern = compile(r"\((.*)\)\s{1}(\d*).*")
      elements = findall(pattern, line)
      # print(elements)
      pymining_dict[elements[0][0].strip()] = elements[0][1]

  # checks if there was a difference
  flag = False

  if len(pymining_dict) >= len(cpp_dict):
    for pattern, count in pymining_dict.items():
      if pattern.strip() not in cpp_dict:
        flag = True
        print("The pattern missing in {filename} is {pat}".format(
            filename=FILE_CPP, pat=pattern))
        continue
    print("Everything matches!") if not flag else print("There were differences!")
  else:
    for pattern, count in cpp_dict.items():
      if pattern.strip() not in pymining_dict:
        flag = True
        print("The pattern missing in {filename} is {pat}".format(
            filename=FILE_PYMINING, pat=pattern))
        continue
    print("Everything matches!") if not flag else print("There were differences!")

  print("Done comparing the results.txt")