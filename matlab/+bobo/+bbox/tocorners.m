function [bb] = tocorners(bb_xywh)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

xmin = bb_xywh(:,1);
ymin = bb_xywh(:,2);
width = bb_xywh(:,3);
height = bb_xywh(:,4);

bb = [xmin ymin xmin+width ymin+height];
