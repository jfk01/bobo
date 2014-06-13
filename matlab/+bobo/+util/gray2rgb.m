function [imrgb] = gray2rgb(imgray)

imrgb = (repmat(imgray,[1 1 3]));