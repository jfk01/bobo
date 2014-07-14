function varargout = gui_video(varargin)
% GUI_VIDEO MATLAB code for gui_video.fig
%      GUI_VIDEO, by itself, creates a new GUI_VIDEO or raises the existing
%      singleton*.
%
%      H = GUI_VIDEO returns the handle to a new GUI_VIDEO or the handle to
%      the existing singleton*.
%
%      GUI_VIDEO('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI_VIDEO.M with the given input arguments.
%
%      GUI_VIDEO('Property','Value',...) creates a new GUI_VIDEO or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before gui_video_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to gui_video_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help gui_video

% Last Modified by GUIDE v2.5 14-Jul-2014 16:02:10

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @gui_video_OpeningFcn, ...
                   'gui_OutputFcn',  @gui_video_OutputFcn, ...
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


% --- Executes just before gui_video is made visible.
function gui_video_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to gui_video (see VARARGIN)

% Choose default command line output for gui_video
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);


% Initialize bounding box
global GUI;
GUI.h_imagesc = [];

% Show image
GUI.currentframe = GUI.startframe;
GUI.is_paused = false; 
GUI.handles = handles;

imdisplay();

% UIWAIT makes gui_video wait for user response (see UIRESUME)
uiwait(handles.gui_videobbox);


function gui_video_OutputFcn(hObject, eventdata, handles, varargin)
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

if ~isempty(GUI.playCallback)
  GUI.playCallback();
end

% Title
title(get(GUI.h_imagesc,'Parent'), sprintf('Video: Frame=[%d/%d/%d], Framerate=%dHz', GUI.startframe,  GUI.currentframe, GUI.endframe, GUI.framerate));
drawnow;


% --- Executes on button press in playbutton.
function playbutton_Callback(hObject, eventdata, handles)
global GUI;
GUI.is_paused = false;
for k=GUI.currentframe:GUI.endframe  
  GUI.currentframe = k;  
  imdisplay();
  pause(1.0 / (GUI.framerate*2.0));
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



% --- Executes on key press with focus on imslider and none of its controls.
function imslider_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to imslider (see GCBO)
% eventdata  structure with the following fields (see UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
