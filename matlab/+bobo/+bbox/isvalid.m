function [is] = isvalid(bb)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

is = (size(bb,2) >= 4) && (bobo.bbox.isxywh(bb));
