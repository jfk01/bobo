function [bb_xywh] = corners2xywh(bb)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

xmin = bb(:,1);
ymin = bb(:,2);
xmax = bb(:,3);
ymax = bb(:,4);

bb_xywh = [xmin ymin xmax-xmin ymax-ymin];

