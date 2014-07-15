function [] = label_shotboundary(indir, outdir)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

%% Defaults
if ~exist('outdir','var') || isempty(outdir)
  outdir = indir;
end


%% Display video
clear global GUI; global GUI; 
GUI.user.outdir = outdir;
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
fprintf('[label_shotboundary]: Saving "%s" and "%s" \n', fullfile(GUI.user.outdir, 'shotboundary.mat'), fullfile(GUI.user.outdir, 'shotboundary.csv'));
save(fullfile(GUI.user.outdir, 'shotboundary.mat'), 'shotboundary');
csvwrite(fullfile(GUI.user.outdir, 'shotboundary.csv'), [find(shotboundary); ones(1,length(find(shotboundary)))]');

