function [iou] = overlap(bb_true, bb_est)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------



%% Input check
if isempty(bb_true)
  iou = zeros(1,size(bb_est,1));  return;  
elseif isempty(bb_est)
  iou = [];  return;
%elseif ~bubo.bbox.isvalid(bb_true) || ~bubo.bbox.isvalid(bb_est)
%  keyboard
%  error('invalid bounding box input');
end


%% Bounding box overlap
iou = zeros(size(bb_true,1), size(bb_est,1));
for i=1:size(bb_true,1)
  for j=i:size(bb_est,1)
    iou(i,j) = bubo.bbox.intersection_over_union(bb_true(i,:), bb_est(j,:));
  end
end


