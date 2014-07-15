function [dlist] = dirlist(indir)
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
  error('Directory ''%s'' not found', imgdir);
end


%% For all files in the provided directory
n_dirs = 0;
dir_files = dir(indir);
dlist = {};
for j=1:length(dir_files)
  % Read current image filename
  if (dir_files(j).isdir == 1) && (dir_files(j).name(1) ~= '.')
    filename = fullfile(indir, dir_files(j).name);
    n_dirs = n_dirs + 1;
    dlist(n_dirs) = {filename};
  end
end

