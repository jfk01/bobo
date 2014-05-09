function [cls] = classification(labels, confidence, do_plot)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------


%% Precision recall
y = labels;
[recall, precision, info] = vl_pr(y, confidence);


%% ROC curve


%% Final stats
cls.y = y;
cls.precision = precision;
cls.recall = recall;
cls.ap = info.ap;
cls.auc = info.auc;


%% Plots
if (do_plot) || (nargout == 0)
  bubo.show.classification(cls);
end

