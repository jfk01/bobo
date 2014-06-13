function [imgout] = imbbox(im, bb, opt)
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
for k=1:size(bb,1)
  hold on; rectangle('Position', bb(k,:), 'LineWidth',opt.linewidth,'EdgeColor',opt.linecolor); hold off;
end
drawnow; 
imgout = [];

