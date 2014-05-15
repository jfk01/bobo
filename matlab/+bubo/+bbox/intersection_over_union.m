function [iou] = intersection_over_union(a, b)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

%% Convert from xywh to corners
a = bubo.bbox.tocorners(a);
b = bubo.bbox.tocorners(b);


%% Overlap!
width = min(a(:,3), b(:,3)) - max(a(:,1), b(:,1));
height = min(a(:,4), b(:,4)) - max(a(:,2), b(:,2));
area_intersection = width.*height;
area_a = (a(:,3)-a(:,1)) .* (a(:,4)-a(:,2));
area_b = (b(:,3)-b(:,1)) * (b(:,4)-b(:,2));
area_union = (area_a + area_b - area_intersection);
iou = area_intersection ./ area_union;
iou(width <= 0) = 0;  % invalid (no overlap)
iou(height <= 0) = 0;  % invalid (no overlap)

