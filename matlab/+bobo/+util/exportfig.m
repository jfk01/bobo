function [filename] = exportfig(filename, h)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

if exist('filename','var')
  filename = sprintf('fig_%s.png', bobo.util.datefile());
end
if ~exist('h','var')  
  figure(h);  
end


%% ./deps/export_fig
export_fig(filename, '-transparent');

