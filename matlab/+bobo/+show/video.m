function [] = video(indir, startframe, endframe, skipframe, framerate, playCallback)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------


%% Input
imlist = bobo.util.imlist(indir);


%% Defaults
if ~exist('startframe', 'var') || isempty(startframe)
  startframe = 1;
end
if ~exist('endframe', 'var') || isempty(endframe)
  endframe = length(imlist);
end
if ~exist('skipframe', 'var') || isempty(skipframe)
  skipframe = 1;
end
if ~exist('framerate', 'var') || isempty(framerate)
  framerate = 60;
end
if ~exist('playCallback', 'var') || isempty(playCallback)
  playCallback = [];
end



%% Video display
global GUI;  % usage annotation
GUI.imlist = imlist;
GUI.startframe = startframe;
GUI.currentframe = GUI.startframe;
GUI.endframe = endframe;
GUI.skipframe = skipframe;
GUI.framerate = framerate;
GUI.playCallback = playCallback;
gui_video();  % ${BOBO}/matlab/gui


