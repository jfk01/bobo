function [] = csvtrack(framenum, trackid, tracklabel, bbox, score, outfile)
%--------------------------------------------------------------------------
%
% Copyright (c) 2014 Jeffrey Byrne
%
%--------------------------------------------------------------------------

% output format is 
% frame_number<int>, track_id<int>, object_type<string>, bounding_box_xmin<int>, bounding_box_ymin<int>, bounding_box_xmax<int>, bounding_box_ymax<int>, detection_score<float>

fprintf('[bobo.annotate.csvtrack] exporting to ''%s''\n', outfile);
f = fopen(outfile, 'w');
for k=1:size(bbox,1)
  fprintf(f, '%d,%d,%s,%d,%d,%d,%d,%f\n', framenum(k), trackid, tracklabel, round(bbox(k,1)), round(bbox(k,2)), round(bbox(k,3)), round(bbox(k,4)), score(k));
end
fclose(f);
