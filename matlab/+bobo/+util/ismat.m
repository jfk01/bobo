function [is] = ismat(filename)

[xxx,ext] = bobo.util.splitext(filename);
is = exist(filename, 'file') && strcmp(ext, '.mat');