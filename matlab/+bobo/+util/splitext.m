function [filepath, fileext] = splitext(filename)

[filepath, fileext] = strtok(filename, '.');