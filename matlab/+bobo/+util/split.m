function [filepath, filename] = split(infile)

[filepath, filebase, ext] = fileparts(infile);
filepath = fullfile(filepath, filebase);
filename = sprintf('%s%s', filebase, ext);

