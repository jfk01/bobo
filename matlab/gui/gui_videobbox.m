function varargout = gui_videobbox(varargin)
% GUI_VIDEOBBOX MATLAB code for gui_videobbox.fig
%      GUI_VIDEOBBOX, by itself, creates a new GUI_VIDEOBBOX or raises the existing
%      singleton*.
%
%      H = GUI_VIDEOBBOX returns the handle to a new GUI_VIDEOBBOX or the handle to
%      the existing singleton*.
%
%      GUI_VIDEOBBOX('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI_VIDEOBBOX.M with the given input arguments.
%
%      GUI_VIDEOBBOX('Property','Value',...) creates a new GUI_VIDEOBBOX or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before gui_videobbox_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to gui_videobbox_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help gui_videobbox

% Last Modified by GUIDE v2.5 22-May-2014 09:48:06

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @gui_videobbox_OpeningFcn, ...
                   'gui_OutputFcn',  @gui_videobbox_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before gui_videobbox is made visible.
function gui_videobbox_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to gui_videobbox (see VARARGIN)

% Choose default command line output for gui_videobbox
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);


% Initialize bounding box
global GUI;
GUI.h_imagesc = [];
if ~isfield(GUI, 'bbox')
  GUI.bbox = NaN(GUI.endframe - GUI.startframe + 1, 4);
  GUI.was_moved = ones(GUI.endframe - GUI.startframe + 1, 1);
end
if ~isfield(GUI, 'is_occluded')
  GUI.is_occluded = zeros(GUI.endframe - GUI.startframe + 1, 1);
end

GUI.imrect = [];

% Show image
GUI.currentframe = GUI.startframe;
GUI.is_paused = false; 
GUI.handles = handles;

imdisplay();

% Give user some feedback
fprintf('[%s]: move or resize bounding box for object of interest\n', mfilename);
fprintf('[%s]: click on scrollbar to jump from keyframe to keyframe\n', mfilename);
fprintf('[%s]: click play to show linearly interpolated bounding boxes for every frame\n', mfilename);
fprintf('[%s]: right click within bounding box to bring up context menu\n', mfilename);
fprintf('[%s]: mark bounding box occluded if object is not visible\n', mfilename);
fprintf('[%s]: when done, close the window (do not hit ctrl-c)\n', mfilename);



% UIWAIT makes gui_videobbox wait for user response (see UIRESUME)
uiwait(handles.gui_videobbox);


function gui_videobbox_OutputFcn(hObject, eventdata, handles, varargin)
return


% --- Display image
function imdisplay()
global GUI;
img = imread(GUI.imlist{GUI.currentframe});
if isempty(GUI.h_imagesc)
  GUI.h_imagesc = imagesc(img);  axis image; axis off;  % first time
else
  set(GUI.h_imagesc, 'CData', img);  % faster 
end
set(GUI.handles.imslider, 'Value', GUI.currentframe);

% display rectange
if isempty(GUI.imrect) 
  if any(isnan(GUI.bbox(GUI.currentframe,:)))
    imrect_CreateFcn([100 100 100 200]);  % create in default position
  else
    imrect_CreateFcn(GUI.bbox(GUI.currentframe,:));  % create in default position
  end
  GUI.bbox(GUI.currentframe,:) = getPosition(GUI.imrect);  
  GUI.is_occluded(GUI.currentframe) = imrect_IsOccludedState();  
elseif any(isnan(GUI.bbox(GUI.currentframe,:))) || (is_keyframe() && (GUI.was_moved(GUI.currentframe) == 0))
  GUI.bbox(GUI.currentframe,:) = getPosition(GUI.imrect);  % current position
  GUI.is_occluded(GUI.currentframe) = imrect_IsOccludedState();
else
  setPosition(GUI.imrect, GUI.bbox(GUI.currentframe,:));  % use stored position (triggers callback)
end
setPosition(GUI.imrect, GUI.bbox(GUI.currentframe,:));  % use stored position (triggers callback)
if GUI.is_occluded(GUI.currentframe)
  setColor(GUI.imrect, 'red');
  set(GUI.imrect_occlusionmenu,'Checked', 'on');
else
  setColor(GUI.imrect, 'blue');
  set(GUI.imrect_occlusionmenu,'Checked', 'off');
end

% Title
title(sprintf('Video Bounding Box [%d/%d/%d]: occluded=%1.1f, xmin=%d, ymin=%d, width=%d, height=%d', GUI.startframe,  GUI.currentframe, GUI.endframe,GUI.is_occluded(GUI.currentframe), round(GUI.bbox(GUI.currentframe,:)))); 
drawnow;


% --- Executes on button press in playbutton.
function playbutton_Callback(hObject, eventdata, handles)
global GUI;
GUI.is_paused = false;
for k=GUI.currentframe:GUI.endframe  
  GUI.currentframe = k;  
  imdisplay();  
  if (GUI.is_paused == true) || (get(handles.playbutton, 'Value') == 0)
    set(handles.playbutton, 'Value', 0);
    imslider_Callback(handles.imslider, [], handles);  % snap to skipframe
    break;
  end
end

% --- Executes on slider movement.
function imslider_Callback(hObject, eventdata, handles)
global GUI;
GUI.currentframe = (floor(get(hObject, 'Value')/GUI.skipframe)*GUI.skipframe) + 1;  % round to nearest frameskip
GUI.is_paused = true;
imdisplay();


% --- Executes during object creation, after setting all properties.
function imslider_CreateFcn(hObject, eventdata, handles)
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end
global GUI;
set(hObject, 'Min', GUI.startframe);
set(hObject, 'Max', GUI.endframe);
set(hObject, 'Value', GUI.currentframe);
set(hObject, 'SliderStep', [GUI.skipframe/(GUI.endframe-GUI.startframe), GUI.skipframe/(GUI.endframe-GUI.startframe)]);


% --- Rectangle creation
function imrect_CreateFcn(bbox)
global GUI;
GUI.imrect = imrect(GUI.handles.imaxis, bbox);  % default position
addNewPositionCallback(GUI.imrect, @imrect_Interpolation);
hrectchild = get(GUI.imrect, 'Children');
hcmenu = get(hrectchild(1),'UIContextMenu');
itemnew = uimenu(hcmenu, 'Label', 'Occluded?', 'Callback', @imrect_OcclusionMenu); 
GUI.imrect_occlusionmenu = itemnew;


% --- Rectangle context menu callback
function imrect_OcclusionMenu(hObject, eventdata, handles)
global GUI;
if strcmp(get(hObject,'Checked'), 'off')
  set(hObject, 'Checked', 'on');
  GUI.is_occluded(GUI.currentframe) = 1;
else
  set(hObject, 'Checked', 'off');
  GUI.is_occluded(GUI.currentframe) = 0;
end  
imdisplay();


% --- Rectangle menu state
function [is] = imrect_IsOccludedState()
global GUI;
if strcmp(get(GUI.imrect_occlusionmenu,'Checked'), 'off')
  is = 0;
else
  is = 1;
end


% --- Rectangle menu state
function [is] = is_keyframe()
global GUI;
if mod(GUI.currentframe-1, GUI.skipframe) == 0
  is = true;
else
  is = false;
end


% --- Rectangle interpolation
function imrect_Interpolation(bbox)
global GUI;
if ~is_keyframe()
  return;
end

% Linear interpolation from keyframes only
bb = bbox;
k = GUI.currentframe;
GUI.bbox(k,:) = bbox;
k_prev = max(GUI.currentframe - GUI.skipframe, 1);
k_next = min(GUI.currentframe + GUI.skipframe, GUI.endframe);
bb_prev = GUI.bbox(k_prev, :);
bb_next = GUI.bbox(k_next, :);

if k_prev == k 
  GUI.bbox(k_prev, :) = GUI.bbox(k, :);
  GUI.is_occluded(k_prev) = GUI.is_occluded(k);
else
  GUI.bbox(k_prev+1:k, 1) = interp1([k_prev k], [bb_prev(1) bb(1)], k_prev+1:k);
  GUI.bbox(k_prev+1:k, 2) = interp1([k_prev k], [bb_prev(2) bb(2)], k_prev+1:k);
  GUI.bbox(k_prev+1:k, 3) = interp1([k_prev k], [bb_prev(3) bb(3)], k_prev+1:k);
  GUI.bbox(k_prev+1:k, 4) = interp1([k_prev k], [bb_prev(4) bb(4)], k_prev+1:k);
  GUI.is_occluded(k_prev+1:k) = interp1([k_prev k], [GUI.is_occluded(k_prev) GUI.is_occluded(k)], k_prev+1:k);  
end
GUI.bbox(k,:) = bbox;

if k_next == k 
  GUI.bbox(k_next, :) = GUI.bbox(k, :);
  GUI.is_occluded(k_next) = GUI.is_occluded(k);
else
  GUI.bbox(k:k_next-1, 1) = interp1([k k_next], [bb(1) bb_next(1)], k:k_next-1);
  GUI.bbox(k:k_next-1, 2) = interp1([k k_next], [bb(2) bb_next(2)], k:k_next-1);
  GUI.bbox(k:k_next-1, 3) = interp1([k k_next], [bb(3) bb_next(3)], k:k_next-1);
  GUI.bbox(k:k_next-1, 4) = interp1([k k_next], [bb(4) bb_next(4)], k:k_next-1);
  GUI.is_occluded(k:k_next-1) = interp1([k k_next], [GUI.is_occluded(k) GUI.is_occluded(k_next)], k:k_next-1);  
end
GUI.bbox(k,:) = bbox;

% Mark moved by user 
GUI.was_moved(GUI.currentframe) = 1;


% --- Executes on key press with focus on imslider and none of its controls.
function imslider_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to imslider (see GCBO)
% eventdata  structure with the following fields (see UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
