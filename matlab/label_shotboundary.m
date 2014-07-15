function [] = label_shotboundary(indir, outfile)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

%% Defaults
if ~exist('outfile','var') || isempty(outfile)
  outfile = 'shotboundary.mat';
end
[filepath,xx] = bobo.util.split(outfile);
bobo.util.remkdir(filepath);


%% Display video
clear global GUI; global GUI; close all;
GUI.user.outfile = outfile;
bobo.show.video(indir,[],[],[],[], @playCallback);


%%-------------------------------------------------------------------------
function [] = playCallback()
global GUI;
if ~isfield(GUI.user, 'figure')
  h = gcf;  
  GUI.user.figure = figure(1000);
  GUI.user.button = uicontrol('Style','pushbutton','String','Shot Boundary', 'Position',[20 10 160 20], 'Callback', @shotCallback);
  GUI.user.savebutton = uicontrol('Style','pushbutton','String','Save', 'Position',[180 10 50 20], 'Callback', @saveCallback);
  GUI.user.axes = gca;
  GUI.user.data = zeros(size(1:GUI.endframe));
  figure(h);      
  shotCallback([],[],[]);
  GUI.user.data(1) = 1;
end


%%-------------------------------------------------------------------------
function [] = shotCallback(hObject, eventdata, handles)
global GUI;
GUI.user.data(GUI.currentframe) = get(GUI.user.button, 'Value');
title(GUI.user.axes, 'Shot Boundary');
xlabel('Frame');  ylabel('Is Shot Boundary?');
bar(GUI.user.axes, GUI.user.data); grid on;


%%-------------------------------------------------------------------------
function [] = saveCallback(hObject, eventdata, handles)
global GUI;
shotboundary = (GUI.user.data);
[filebase, xx] = bobo.util.splitext(GUI.user.outfile);
fprintf('[label_shotboundary]: Saving "%s.*"\n', filebase);
save(sprintf('%s.mat', filebase), 'shotboundary');
csvwrite(sprintf('%s.csv', filebase), [find(shotboundary); ones(1,length(find(shotboundary)))]');

