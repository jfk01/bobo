function [vidlist] = videolist(indir, use_extensions)
%--------------------------------------------------------------------------
%
% Copyright (c) 201 Jeffrey Byrne
% $Id: imglist.m 82 2012-08-11 21:58:47Z jebyrne $
%
%--------------------------------------------------------------------------

%% Error checks
if (nargin < 1)
  error('Must include directory for list creation');
end
if (exist(indir, 'dir') == 0)
  error('Directory ''%s'' not found', indir);
end
if (~exist('use_extensions', 'var') || isempty(use_extensions))
  use_extensions = {'.mp4','.avi', '.mpeg', '.mov'};
end


%% For all files in the provided directory
dir_files = dir(indir);
num_videos = 0;
vidlist = {};
for j=1:length(dir_files)
  % Read current image filename
  [x,filebase,ext] = fileparts(dir_files(j).name);
  if (dir_files(j).isdir == 0) && ~isempty(ext) && ~isempty(strmatch(ext, use_extensions)) && (filebase(1) ~= '.')
    filename = strcat(indir,filesep,dir_files(j).name);
    num_videos = num_videos + 1;
    vidlist(num_videos) = {filename};
  end
end

