function [det] = detection(bb_true, bb_est, score, min_overlap, do_plot)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------


%% Ground truth labels (minimum bounding box overlap with ground truth)
for k=1:length(bb_true)
  y{k} = 2*double(sum(double(bubo.bbox.overlap(bb_true{k}, bb_est{k}) >= min_overlap), 1) > 0) - 1;  % [-1, 1]
end
y = cell2mat(y)';
score = cell2mat(score)';


%% Precision recall
[recall, precision, info] = vl_pr(y, score);


%% ROC curve


%% Final stats
det.y = y;
det.precision = precision;
det.recall = recall;
det.ap = info.ap;
det.auc = info.auc;


%% Plots
if (do_plot) || (nargout == 0)
  bubo.show.detection(det);
end

