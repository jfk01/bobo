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
x1 = max(a(:,1), b(1));
y1 = max(a(:,2), b(2));
x2 = min(a(:,3), b(3));
y2 = min(a(:,4), b(4));

w = x2-x1+1;
h = y2-y1+1;
area_intersection= w.*h;
area_a = (a(:,3)-a(:,1)+1) .* (a(:,4)-a(:,2)+1);
area_b = (b(3)-b(1)+1) * (b(4)-b(2)+1);
area_union = (area_a + area_b - area_intersection);
iou = a_intersection ./ area_union;
iou(w <= 0) = 0;  % invalid (no overlap)
iou(h <= 0) = 0;  % invalid (no overlap)


