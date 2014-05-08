function [bb_struct] = bb2struct(bb)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

xmin = bb(:,1);
ymin = bb(:,2);
xmax = bb(:,3);
ymax = bb(:,4);

bb_struct.xmin = xmin;
bb_struct.xmax = xmax;
bb_struct.ymin = ymin;
bb_struct.ymax = ymax;
bb_struct.width = xmax-xmin;
bb_struct.height = xmax-xmin;
bb_struct.bbox = bb;

