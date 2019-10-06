import scipy.io as sio
import numpy as np
import json
import os


def load_data(data_name):
    data = sio.loadmat(data_name)
    prediction = data['prediction'][0,0]
    name, im_sz, left, right, left_cnn, right_cnn, deep, stat, seglines = prediction
   
    name = name[0]
    im_sz = im_sz[0].tolist()
    stat = stat[0,0]
    vps_homo, zen_homo, zengroup, horgroup, vpsgroup, horCandidates_homo, \
    horCandidateScores, maxHorCandidateId, allCandidates = stat

    # seglines: number x 4 (two endpoints)
    line_segs = seglines.tolist()

    # vps_homo: 3 x number_vps
    vps = np.array([vps_homo[0] / vps_homo[2], vps_homo[1] / vps_homo[2]]).T.tolist()
    
    # vpsgroup = vpsgroup[0]
    group_ind = []
    for i, item in enumerate(vpsgroup):
        if i == 0:
            ind = item[0].tolist()[0]
        else:
            ind = item[0].T.tolist()[0]
        group_ind.append(ind)

    return name, im_sz, line_segs, vps, group_ind


def group2group(group, line_number):
    # group: group_number x ind
    group_output = -np.ones(line_number).astype(np.int)
    group_number = len(group)
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
        image_path, image_size, line_segs, vps, group = load_data(data_name)
        # there are overlap for each group
        # image_size: height x width
        
        fake_focal = max(image_size) / 2
        vps_output = []
        for vp in vps:
            new_vp = [(vp[1] * fake_focal ) / (image_size[0] / 2), (vp[0] * fake_focal) / (image_size[1] / 2)]
            vps_output.append(new_vp)

        line_segs_output, new_lines_output = lineseg2line(line_segs, image_size)
        group_output = group2group(group, len(line_segs))

        image_name = image_path.split('/')[-1]
        json_out = {'image_path': image_name, 'line': new_lines_output, 'org_line': line_segs_output, 
                'group': group_output, 'vp': vps_output} 

        json.dump(json_out, save_op)
        save_op.write('\n')


if __name__ == '__main__':
    path = '/n/fs/vl/xg5/workspace/baseline/gc-horizon-detector/outputs'
    data_list = [os.path.join(path, item) for item in os.listdir(path)]
    
    save_path = 'data/data.json'
    process(data_list, save_path)
    

