#!/usr/bin/env python3
import fileinput

with fileinput.FileInput("polbooks.txt", inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace("a", " "), end='')