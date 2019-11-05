import os
import json
import numpy as np


if __name__ == '__main__':
    task_name = 'YUD'
    if task_name == 'YUD':
        gt_file = '/n/fs/vl/xg5/Datasets/YUD/label/test.txt'
        height = 480
    elif tesk_name == 'ScanNet':
        gt_file = '/n/fs/vl/xg5/Datasets/ScanNet/label/test.txt'
        height = 512
    elif tesk_name == 'SceneCityUrban3D':
        gt_file = '/n/fs/vl/xg5/Datasets/SceneCityUrban3D/label/test.txt'
        height = 512
    elif tesk_name == 'SUNCG':
        gt_file = '/n/fs/vl/xg5/Datasets/SUNCG/label/test.txt'
        height = 480
    else:
        raise ValueError('No such task!')
        
    pred_file = '../../result/' + task_name + '.txt'
    save_file = '../../result/' + task_name + '.json'
    with open(gt_file, 'r') as op: gt_content = op.readlines()
    with open(pred_file, 'r') as op: pred_content = op.readlines()
    assert(len(gt_content) == len(pred_content))
    
    with open(save_file, 'w') as save_op:
        for i in range(len(gt_content)):
            gt_line = gt_content[i]
            pred_line = pred_content[i]
            gt_list = gt_line.split(' ')
            image_name = gt_list[0]
            gt_fov = float(gt_list[1])
            pred_fov = float(pred_line)
        
            gt_focal = float(height / (2 * np.tan(gt_fov / 2)))
            pred_focal = float(height / (2 * np.tan(pred_fov / 2)))
    
            json_out = {'image_name': image_name, 'focal_gt': gt_focal, 'focal_pred': pred_focal}
            
            json.dump(json_out, save_op)
            save_op.write('\n')
    
