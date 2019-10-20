clear
close all

addpath util
addpath /home/guoxin/caffe/matlab


datapath = '/n/fs/vl/xg5/Datasets/YUD/YorkUrbanDB';
savepath = 'dataset/YUD/output';

dirs = dir(datapath);

img_list = {};
for i = 3:size(dirs,1)
    dir_name = dirs(i).name;
    dirpath = [datapath, '/', dir_name];
    if isdir(dirpath)
        image_name = [dirpath, '/', dir_name, '.jpg'];
        img_list = [img_list; image_name];
    end
end


% get default configuration
opt = default_option();

compute_horizon(img_list, savepath, opt);

%{
imgDir = 'assets/imgs/';  % directory of input images
outDir = 'outputs/';      % directory for storing results

imgList = glob([imgDir, '*.jpg']);

% get default configuration
opt = default_option();

compute_horizon(imgList, outDir, opt);

end
%}
