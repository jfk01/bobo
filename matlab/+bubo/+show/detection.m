function [det] = detection(det)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

%% Inputs
if ~isstruct(det) || ~isfield(det, 'precision')
  error('input must be the output from bubo.eval.detection');
end


%% Parameters
str_plotstyle = [{'b-'}, {'g-'}, {'r-'}, {'k-'}; {'b-.'}, {'g-.'}, {'r-.'}, {'k-.'}]';


%% Plots
figure(1); clf; hold on;
plot(det.recall, det.precision);
grid on; xlabel 'Recall'; ylabel 'Precision'


