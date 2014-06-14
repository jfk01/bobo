function [det] = detection(det)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

%% Inputs
if ~isstruct(det) || ~isfield(det, 'precision')
  error('input must be the output from bobo.eval.detection');
end


%% Parameters
str_plotstyle = [{'b-'}, {'g-'}, {'r-'}, {'k-'}; {'b-.'}, {'g-.'}, {'r-.'}, {'k-.'}]';


%% Plots
figure; clf; hold on;
plot(det.recall, det.precision);
axis([0 1 0 1]);
grid on; xlabel 'Recall'; ylabel 'Precision'


