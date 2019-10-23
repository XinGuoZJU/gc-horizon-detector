clear
close all

addpath util
addpath /home/guoxin/caffe/matlab

dataset_name = 'YUD';
if strcmp(dataset_name, 'YUD')
    datapath = '/n/fs/vl/xg5/Datasets/YUD/YorkUrbanDB';
    savepath = 'dataset/YUD/output';
    img_type = 'jpg';
elseif strcmp(dataset_name, 'scannet')
    datapath = '/n/fs/vl/xg5/Datasets/neurodata/scannet-vp';
    savepath = 'dataset/scannet-vp/output';
    img_type = 'png';
end

dirs = dir(datapath);  % struct

img_list = {};
for i = 3:size(dirs,1)
    dir_name = dirs(i).name;
    dirpath = [datapath, '/', dir_name];
    if isdir(dirpath)
        image_list = dir([dirpath, '/*.', img_type]);  % struct
        for j = 1: size(image_list,1)
            img_name = image_list(j).name;
            image_name = [dirpath, '/', img_name];
            img_list = [img_list; image_name];
        end
    end
end


% get default configuration
opt = default_option();

compute_horizon(img_list, savepath, opt);

