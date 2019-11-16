function main2(dataset_name, idx)

addpath util
addpath /home/guoxin/caffe/matlab

%dataset_name = 'YUD';
%idx = 0;

tic
if strcmp(dataset_name, 'YUD')
    index_file = ['/n/fs/vl/xg5/Datasets/YUD/label/index_', num2str(idx), '.txt'];
    datapath = '/n/fs/vl/xg5/Datasets/YUD/YorkUrbanDB';
    savepath = 'dataset/YUD/output';
    img_type = 'jpg';
elseif strcmp(dataset_name, 'ScanNet')
    index_file = ['/n/fs/vl/xg5/Datasets/ScanNet/label/index_', num2str(idx), '.txt'];
    datapath = '/n/fs/vl/xg5/Datasets/ScanNet/scannet-vp';
    savepath = 'dataset/ScanNet/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'SceneCityUrban3D')
    index_file = ['/n/fs/vl/xg5/Datasets/SceneCityUrban3D/label/index_', num2str(idx), '.txt'];
    datapath = '/n/fs/vl/xg5/Datasets/SceneCityUrban3D/su3';
    savepath = 'dataset/SceneCityUrban3D/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'SUNCG')
    index_file = ['/n/fs/vl/xg5/Datasets/SUNCG/label/index_', num2str(idx), '.txt'];
    datapath = '/n/fs/vl/xg5/Datasets/SUNCG/mlt_v2';
    savepath = 'dataset/SUNCG/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'ScanNet_error')
    index_file = ['/n/fs/vl/xg5/workspace/baseline/gc_horizon_detector/tools/error_case/ScanNet_', num2str(idx), '.txt']; 
    datapath = '/n/fs/vl/xg5/Datasets/ScanNet/scannet-vp';
    savepath = 'dataset/ScanNet/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'SceneCityUrban3D_error')
    index_file = ['/n/fs/vl/xg5/workspace/baseline/gc_horizon_detector/tools/error_case/SceneCityUrban3D_', num2str(idx), '.txt']; 
    datapath = '/n/fs/vl/xg5/Datasets/SceneCityUrban3D/su3';
    savepath = 'dataset/SceneCityUrban3D/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'SUNCG_error')
    index_file = ['/n/fs/vl/xg5/workspace/baseline/gc_horizon_detector/tools/error_case/SUNCG_', num2str(idx), '.txt']; 
    datapath = '/n/fs/vl/xg5/Datasets/SUNCG/mlt_v2';
    savepath = 'dataset/SUNCG/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'ScanNet_aug')
    index_file = ['/n/fs/vl/xg5/Datasets/ScanNet_aug/label/index_', num2str(idx), '.txt'];
    datapath = '/n/fs/vl/xg5/Datasets/ScanNet_aug/image';
    savepath = 'dataset/ScanNet_aug/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'SceneCityUrban3D_aug')
    index_file = ['/n/fs/vl/xg5/Datasets/SceneCityUrban3D_aug/label/index_', num2str(idx), '.txt'];
    datapath = '/n/fs/vl/xg5/Datasets/SceneCityUrban3D_aug/image';
    savepath = 'dataset/SceneCityUrban3D_aug/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'SUNCG_aug')
    index_file = ['/n/fs/vl/xg5/Datasets/SUNCG_aug/label/index_', num2str(idx), '.txt'];
    datapath = '/n/fs/vl/xg5/Datasets/SUNCG_aug/image';
    savepath = 'dataset/SUNCG_aug/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'ScanNet_aug_error')
    index_file = ['/n/fs/vl/xg5/workspace/baseline/gc_horizon_detector/tools/error_case/ScanNet_', num2str(idx), '.txt']; 
    datapath = '/n/fs/vl/xg5/Datasets/ScanNet/scannet-vp';
    savepath = 'dataset/ScanNet/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'SceneCityUrban3D_aug_error')
    index_file = ['/n/fs/vl/xg5/workspace/baseline/gc_horizon_detector/tools/error_case/SceneCityUrban3D_', num2str(idx), '.txt']; 
    datapath = '/n/fs/vl/xg5/Datasets/SceneCityUrban3D/su3';
    savepath = 'dataset/SceneCityUrban3D/output';
    img_type = 'png';
elseif strcmp(dataset_name, 'SUNCG_aug_error')
    index_file = ['/n/fs/vl/xg5/workspace/baseline/gc_horizon_detector/tools/error_case/SUNCG_', num2str(idx), '.txt']; 
    datapath = '/n/fs/vl/xg5/Datasets/SUNCG/mlt_v2';
    savepath = 'dataset/SUNCG/output';
    img_type = 'png';
end


img_list = {};
fpn = fopen(index_file, 'r');
while ~feof(fpn)
    line_str = fgetl(fpn);
    str_list = strsplit(line_str);
    img_name = str_list{1};

    image_name = [datapath, '/', img_name];
    img_list = [img_list; image_name];
end


% get default configuration
opt = default_option();

compute_horizon(img_list, savepath, opt, dataset_name, num2str(idx));

toc
