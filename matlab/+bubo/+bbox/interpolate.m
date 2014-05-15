function [bb] = interpolate(bb_from, bb_to, n_interp)
%--------------------------------------------------------------------------
%
% Copyright (c) 2012 Jeffrey Byrne
%
%--------------------------------------------------------------------------

k_interp = 0:(1/n_interp):1; 

bb(1,:) = interp1([0 1], [bb_from(1) bb_to(1)], k_interp);
bb(2,:) = interp1([0 1], [bb_from(2) bb_to(2)], k_interp);
bb(3,:) = interp1([0 1], [bb_from(3) bb_to(3)], k_interp);
bb(4,:) = interp1([0 1], [bb_from(4) bb_to(4)], k_interp);

