function [det] = detection(BB_true, BB_est, confidence, min_overlap, do_plot)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------
%
% Input: cell array of detections, ground truth bounding boxes and scores
% All bounding boxes are in matlab (x y w h) format
%
%--------------------------------------------------------------------------


%% Detection assignment 
for k=1:length(BB_est)  
  bb_est = BB_est{k};  bb_true = BB_true{k};  c = confidence{k};
  n_pos(k) = size(bb_true,1);  
  [xx, j] = sort(c,'descend');  bb_est = bb_est(j,:);  % sorted order of decreasing confidence
  
  % Assign best detection to each ground truth bounding box
  n_est = size(bb_est,1);
  tp{k} = zeros(n_est,1);
  fp{k} = zeros(n_est,1);
  overlap = bubo.bbox.overlap(bb_true, bb_est);
  for j=1:n_est
    j_asgn = find(double(overlap(:,j) >= min_overlap));      
    if ~isempty(j_asgn)
      if tp{k}(j_asgn(1)) == 0
        tp{k}(j_asgn(1)) = 1;  % best detection is true positive      
      else
        fp{k}(j_asgn(1)) = 1;  % multiple detections!  
      end  
      if length(j_asgn) > 1
        fp{k}(j_asgn(2:end)) = 1;  % all remaining detections with minimum overlap are false positives      
      end
    else
      fp{k}(j) = 1;  % no detection
    end
  end    
end


%% Precision-recall
[confidence,k] = sort(cell2mat(confidence'), 'descend');
fp = cell2mat(fp');  fp = cumsum(fp(k));
tp = cell2mat(tp');  tp = cumsum(tp(k));
n_pos = sum(n_pos);
recall = tp ./ n_pos;
precision = tp ./ (fp + tp);
ap = sum(precision(find(diff(recall)) + 1 )) / n_pos ;  % average precision (see also vl_pr.m)
auc = 0.5 * sum((precision(1:end-1) + precision(2:end)) .* diff(recall));  % area under curve (see also vl_pr.m)


%% ROC curve


%% Final stats
det.tp = tp;
det.fp = fp;
det.n_pos = n_pos;
det.precision = precision;
det.recall = recall;
det.confidence = confidence;
det.ap = ap;
det.auc = auc;


%% Plots
if (do_plot) || (nargout == 0)
  bubo.show.detection(det);
end

