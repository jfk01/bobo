function [] = label_trackstart(indir, outfile, keyframefile)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

%% Defaults
if ~exist('outfile','var') || isempty(outfile)
  outfile = './tracks.csv';
end


%% Figure
h = figure(1000); clf;
typePopupmenu = uicontrol('Style','popupmenu','String',{'person','vehicle','weapon'}, 'Position',[10 10 100 20], 'Callback', @typeCallback);
newButton = uicontrol('Style','pushbutton','String','New', 'Position',[110 10 50 20], 'Callback', @newCallback);
prevButton = uicontrol('Style','pushbutton','String','<]', 'Position',[170 10 20 20], 'Callback', @prevCallback);
nextButton = uicontrol('Style','pushbutton','String','[>', 'Position',[190 10 20 20], 'Callback', @nextCallback);
saveButton = uicontrol('Style','pushbutton','String','Save', 'Position',[210 10 50 20], 'Callback', @saveCallback);


%% Keyframes
if bobo.util.ismat(keyframefile)
  mat = load(keyframefile);
  keyframes = find(mat.shotboundary);
elseif bobo.util.iscsv(keyframefile)
  mat = csvread(keyframefile);
  keyframes = mat(:,1);
else
  error('invalid keyframe file "%s"', keyframefile);
end
keyframes = [1; keyframes(1:end-1)];  % beginning of shot


%% Parameters
global GUI;
GUI.keyframes = keyframes;
GUI.outfile = outfile;
GUI.indir = indir;
GUI.imlist = bobo.util.imlist(indir);
GUI.currentframe = 1;
GUI.imrect = [];
GUI.tracklist = cell(1,length(GUI.imlist));


%% Initialization
typeCallback(typePopupmenu,[],[]);
show();


%%-------------------------------------------------------------------------
function [] = newCallback(hObject, eventdata, handles)
global GUI;
h = imrect;
h.setColor(labelcolor(GUI.label));
p = h.getPosition();
h_text = text(p(1), p(2), GUI.label, 'BackgroundColor', 'white');
addNewPositionCallback(h, @(p) set(h_text, 'Position', [p(1), p(2), 0])); 
set(h,'UserData', GUI.label);
GUI.imrect = [GUI.imrect h];


%%-------------------------------------------------------------------------
function [] = prevCallback(hObject, eventdata, handles)
global GUI;
cache();
GUI.currentframe = max(GUI.currentframe - 1, 1);
show();
fetch();


%%-------------------------------------------------------------------------
function [] = nextCallback(hObject, eventdata, handles)
global GUI;
cache();
GUI.currentframe = min(GUI.currentframe + 1, length(GUI.keyframes));
show();
fetch();


%%-------------------------------------------------------------------------
function [] = typeCallback(hObject, eventdata, handles)
global GUI;
labels = get(hObject,'String');
GUI.labelindex = get(hObject,'value');
GUI.label = labels{GUI.labelindex};

%%-------------------------------------------------------------------------
function [] = saveCallback(hObject, eventdata, handles)
global GUI;
cache(); show(); fetch();
fprintf('[label_trackstart]: saving "%s"\n', GUI.outfile);
f = fopen(GUI.outfile, 'w');
for k=1:length(GUI.tracklist)
  t = GUI.tracklist{k};
  for j=1:length(t)    
    fprintf(f, '%d,%s,%d,%d,%d,%d\n', k, t(j).label, round(t(j).position(1)), round(t(j).position(2)), round(t(j).position(3)), round(t(j).position(4)));
  end
end
fclose(f);


%%-------------------------------------------------------------------------
function [] = cache()
global GUI;
GUI.tracklist{GUI.currentframe} = [];
for k=1:length(GUI.imrect)
  t.position = GUI.imrect(k).getPosition();
  t.label = get(GUI.imrect(k), 'UserData');  
  GUI.tracklist{GUI.currentframe} = [GUI.tracklist{GUI.currentframe} t];
end

%%-------------------------------------------------------------------------
function [] = show()
global GUI;
imagesc(imread(GUI.imlist{GUI.keyframes(GUI.currentframe)})); axis image;
title(sprintf('Frame: %d', GUI.keyframes(GUI.currentframe)));


%%-------------------------------------------------------------------------
function [] = fetch()
global GUI;
t = GUI.tracklist{GUI.currentframe};
GUI.imrect = [];
for k=1:length(t)
  h = imrect(gca, t(k).position);
  p = h.getPosition();
  h_text = text(p(1), p(2), t(k).label, 'BackgroundColor', 'white');
  addNewPositionCallback(h, @(p) set(h_text, 'Position', [p(1), p(2), 0]));
  h.setColor(labelcolor(t(k).label));  
  set(h, 'UserData', t(k).label);
  GUI.imrect = [GUI.imrect h];
end


%%-------------------------------------------------------------------------
function [color] = labelcolor(label)
if strcmp(label, 'vehicle')
  color = 'green';
elseif strcmp(label, 'person')
  color = 'blue';
elseif strcmp(label, 'weapon')
  color = 'red';
else
  color = 'black';
end

