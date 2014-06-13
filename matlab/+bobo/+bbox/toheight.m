function [bb] = toheight(bb_corners)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

if isempty(bb_corners)
  bb = []; return;
end

xmin = bb_corners(:,1);
ymin = bb_corners(:,2);
xmax = bb_corners(:,3);
ymax = bb_corners(:,4);

bb = [xmin ymin xmax-xmin ymax-ymin];  % (x,y,width,height)

