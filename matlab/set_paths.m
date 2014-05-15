function [] = set_paths()
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------


%% Disable name conflicts during
warning('off','MATLAB:dispatcher:nameConflict');  


%% Support paths
addpath(pwd);
addpath(fullfile(pwd, 'gui'));


%% Unpack Dependencies
deps = {'lightspeed-2.3.1','vlfeat-0.9.16','export_fig-0.2'};
for k=1:length(deps)
  % Unpack
  depdir = fullfile(pwd,'deps',deps{k});
  if ~exist(depdir,'dir')
    fprintf('[%s]: Unpacking %s\n', mfilename, depdir);
    zipfile = strcat(depdir,'.zip');
    unzip(zipfile, depdir);
  end

  % Paths
  fprintf('[%s]: Adding path %s\n', mfilename, depdir');
  addpath(genpath(depdir),'-begin');
end

%% Compile MEX
% try
%   run('compile_mex.m');
% catch ME
%   fprintf('[%s]: WARNING - compiling mex files failed!  Try running compile_mex.m to track down the problem', mfilename);
%   fprintf('[%s]: WARNING - mex files are not needed for seedoflife demos, but some optional tests or evaluations will not run', mfilename);
% end


%% Restore
warning('on','MATLAB:dispatcher:nameConflict');  

