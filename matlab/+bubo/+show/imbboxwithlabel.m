function [imgout] = imbboxwithlabel(im, bb, str_label, opt)
%--------------------------------------------------------------------------
%
% Copyright (c) 2011 Jeffrey Byrne
%
%--------------------------------------------------------------------------

%% Options
if ~exist('opt','var')
  opt.linewidth = 2; 
  opt.linecolor = [0 1 0];  
end

%% Display me
h = figure(sum(char(mfilename)));
set(h,'NumberTitle','off','Toolbar','none','Menubar','none','Name','Detection');
imagesc(im); axis image; colormap(gray); 
hold on;
for k=1:size(bb,1)  
  rectangle('Position', bb(k,:), 'LineWidth', opt.linewidth, 'EdgeColor', opt.linecolor); 
  if iscell(str_label), str=str_label{k}; else, str=str_label; end
  text(bb(k,1)+5, bb(k,2)+12, str, 'BackgroundColor', [1 1 1]);     
end
hold off;
drawnow; 
imgout = [];

