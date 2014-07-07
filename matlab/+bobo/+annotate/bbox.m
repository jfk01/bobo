function [bbox] = bbox(imfile)
%--------------------------------------------------------------------------
%
% Copyright (c) 2012 Jeffrey Byrne
%
%--------------------------------------------------------------------------


imagesc(imread(imfile));  axis equal; 
bbox = round(getrect());

