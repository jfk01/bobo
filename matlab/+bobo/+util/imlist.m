function [imglist] = imlist(imgdir, do_dedupe, use_extensions)
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
if (exist(imgdir, 'dir') == 0)
  error('Directory ''%s'' not found', imgdir);
end
if (~exist('do_dedupe', 'var') || isempty(do_dedupe))
  do_dedupe = false;
end
if (~exist('use_extensions', 'var') || isempty(use_extensions))
  use_extensions = {'.jpg','.png','.tif','.pgm'};
end


%% For all files in the provided directory
dir_files = dir(imgdir);
num_imgs = 0;
imglist = {};
imlast = [];
for j=1:length(dir_files)
  % Read current image filename
  [x,x,ext] = fileparts(dir_files(j).name);
  if (dir_files(j).isdir == 0) && ~isempty(ext) && ~isempty(strmatch(ext, use_extensions))
    filename = strcat(imgdir,filesep,dir_files(j).name);
    if do_dedupe 
      im = nmd.util.im2gray(filename);
      if (isempty(imlast) == true) || (any(abs(im(:) - imlast(:)) > 2E-1))
        imlast = im;
        num_imgs = num_imgs + 1;
        imglist(num_imgs) = {filename};
      end      
    else      
      num_imgs = num_imgs + 1;
      imglist(num_imgs) = {filename};
    end
  end
end

% Error check
if (num_imgs == 0) 
  error(sprintf('No images found in ''%s''', imgdir));
end

