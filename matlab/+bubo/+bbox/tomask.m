function [immask] = bbox2mask(im, bbox)

immask = zeros(size(im));
bbox = round(bbox);
for j=1:size(bbox,1)
  imin = max(bbox(j,2),1);
  imax = min(bbox(j,4),size(im,1));
  jmin = max(bbox(j,1),1);
  jmax = min(bbox(j,3),size(im,2));  
  immask(imin:imax, jmin:jmax) = 1;
end
