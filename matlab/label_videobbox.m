function [outfile] = label_videobbox(indir)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

[bbox, is_occluded] = bobo.annotate.videobbox(indir, 1, fullfile(indir, 'detections.csv'));
