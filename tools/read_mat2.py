import scipy.io as sio
import numpy as np
import json
import os
import math


def load_data(data_name):
    data = sio.loadmat(data_name)
    prediction = data['prediction'][0,0]
    name, im_sz, left, right, left_cnn, right_cnn, deep, stat, seglines = prediction
     
    name = name[0]
    im_sz = im_sz[0].tolist()
    stat = stat[0, 0]
    
    try:
        len(stat)
    except:
        return [], [], []
    vps_homo, zen_homo, zengroup, horgroup, vpsgroup, horCandidates_homo, \
    horCandidateScores, maxHorCandidateId, allCandidates = stat
    
    # In vps_homo, the first one is zen_home, others are horizon vps.
    
    # vps_homo: 3 x number_vps, the first vp is veritcal, others are horizon vps sorted by scores.
    vps = np.array([vps_homo[0] / vps_homo[2], vps_homo[1] / vps_homo[2]]).T.tolist()
    vps = vps[:3]
    
    return name, im_sz, vps


def group2group(group, line_number):
    # group: group_number x ind
    group_output = -np.ones(line_number).astype(np.int)
    group_number = len(group)
    # group_number = min(3, len(group))
    for g in range(group_number):
        for ind in group[g]:
            group_output[ind - 1] = g

    return group_output.tolist() 


def point2line(end_points):
    # line: ax + by + c = 0, in which a^2 + b^2=1, c>0
    # point: 2 x 2  # point x dim
    # A = np.matrix(end_points) - np.array(image_size) / 2
    # result = np.linalg.inv(A) * np.matrix([1,1]).transpose()

    A = np.asmatrix(end_points)
    result = np.linalg.inv(A) * np.asmatrix([-1, -1]).transpose()  # a, b, 1
    a = float(result[0])
    b = float(result[1])
    norm = (a ** 2 + b ** 2) ** 0.5
    result = np.array([a / norm, b / norm, 1 / norm])

    return result


def lineseg2line(line_segs, image_size):
    # line_segs: number x (width, heigth)
    height, width = image_size
    new_line_segs = []
    new_lines = []
    for line_s in line_segs:
        end_points = [[line_s[1], line_s[0]], [line_s[3], line_s[2]]]
        new_line_segs.append(end_points)
        new_end_points = [[(end_points[i][0] - image_size[0] / 2 ) / (image_size[0] / 2),
                            (end_points[i][1] - image_size[1] / 2 ) / (image_size[1] / 2)]
                            for i in range(2)]
        new_line = point2line(new_end_points).tolist()
        new_lines.append(new_line)

    return new_line_segs, new_lines
        

def process(data_list, save_path):
    save_op = open(save_path, 'w')

    for data_name in data_list:
        print(data_name)
        image_path, image_size, vps = load_data(data_name)
        # there are overlap for each group
        # image_size: height x width
        
        if len(vps) < 2:
            continue

        fake_focal = max(image_size) / 2
        vps_output = []
        for vp in vps:
            new_vp = [(vp[1] * fake_focal ) / (image_size[0] / 2), (vp[0] * fake_focal) / (image_size[1] / 2)]
            vps_output.append(new_vp)

        image_names = image_path.split('/')
        image_name = os.path.join(image_names[-2], image_names[-1])
        
        json_out = {'image_path': image_name, 'vp': vps_output} 

        json.dump(json_out, save_op)
        save_op.write('\n')


if __name__ == '__main__':
    data_name = 'ScanNet'   # 'YUD', 'ScanNet', 'SceneCityUrban3D', 'SUNCG'

    path = '/n/fs/vl/xg5/workspace/baseline/gc_horizon_detector/dataset/' + data_name + '/output'
    dir_list = [os.path.join(path, dir_path) for dir_path in os.listdir(path)]
    data_list = []
    for dirs in dir_list:
        data_list += [os.path.join(dirs, dir_path + '/data.mat') for dir_path in os.listdir(dirs)]

    save_path = '/n/fs/vl/xg5/workspace/baseline/gc_horizon_detector/dataset/' + data_name + '/data'
    os.makedirs(save_path, exist_ok=True)
    save_file = os.path.join(save_path, 'data.json')

    process(data_list, save_file)
    

