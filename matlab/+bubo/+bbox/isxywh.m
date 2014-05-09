function [is] = isxywh(bb)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------


if all((bb(:,3) > bb(:,1)) & (bb(:,4) > bb(:,2)))
  is = false; % (xmin,ymin,xmax,ymax) corners format 
else
  is = true;
end
