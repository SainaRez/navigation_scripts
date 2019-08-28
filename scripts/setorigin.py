from __future__ import division
from pyquaternion import Quaternion
from tf.transformations import quaternion_matrix
from tf.transformations import quaternion_from_matrix
import numpy as np


def average_pose():
    
    f_vicon = open('vicon_transforms.txt','r')
    f_vins = open('vins_transforms.txt','r')

    vicon = [0,0,0,0,0,0,0]
    vins = [0,0,0,0,0,0,0]

    j = 1
    while j < 19:
        #print "line number: ", j 
        line_vicon = f_vicon.readline()
        line_vins = f_vins.readline()
        temp_vicon = line_vicon.split(" ")
        temp_vins = line_vins.split(" ")

        #print "vicon length", len(temp_vicon)
        #print "vins length", len(temp_vins)
        
        for i in range(0, 7):
            #print i
            try:
                vicon[i] = vicon[i] + float(temp_vicon[i])
                vins[i] = vins[i] + float(temp_vins[i])
            except ValueError,e:
                print "error:",e,"on line",j,"index:",i

        # normalize quat
        qlen = vicon[3] + vicon[4] + vicon[5] + vicon[6]
        vicon[3] /= qlen
        vicon[4] /= qlen
        vicon[5] /= qlen
        vicon[6] /= qlen

        # normalize quat
        qlen = vins[3] + vins[4] + vins[5] + vins[6]
        vins[3] /= qlen
        vins[4] /= qlen
        vins[5] /= qlen
        vins[6] /= qlen

        j = j + 1    
                
    for i in range(0, 7):
        vicon[i] = vicon[i]/j-1
        vins[i] = vins[i]/j-1

    #print "vicon: ", vicon
    #print "vins: ", vins

    return vicon, vins

def average_pose_slerp():
    f_vicon = open('vicon_transforms.txt','r')
    f_vins = open('vins_transforms.txt','r')

    vicon_trans = [0,0,0]
    vins_trans = [0,0,0]
    average_vicon_rot = []
    average_vins_rot = []

    j = 1
    while j < 19:
        #print "line number: ", j 
        line_vicon = f_vicon.readline()
        line_vins = f_vins.readline()
        temp_vicon = line_vicon.split(" ")
        temp_vins = line_vins.split(" ")
        vicon_rot = []
        vins_rot = []

        for i in range(0,3):
            vicon_trans[i] = vicon_trans[i] + float(temp_vicon[i])
            vins_trans[i] = vins_trans[i] + float(temp_vins[i])
        for i in range(3,7):
            vicon_rot.append(float(temp_vicon[i]))
            vins_rot.append(float(temp_vins[i]))

        if j == 1:
            average_vicon_rot = Quaternion(np.array(vicon_rot))
            average_vins_rot = Quaternion(np.array(vins_rot))
        else:
            average_vicon_rot = Quaternion.slerp(average_vicon_rot, (Quaternion(np.array(vicon_rot))), 0.5)
            average_vins_rot = Quaternion.slerp(average_vins_rot, (Quaternion(np.array(vins_rot))), 0.5)
                    
        j = j + 1
    

    for i in range(0, 3):
        vicon_trans[i] = vicon_trans[i]/j-1
        vins_trans[i] = vins_trans[i]/j-1

    vicon = np.append(np.array(vicon_trans), (average_vicon_rot.elements))
    vins = np.append(np.array(vins_trans), (average_vins_rot.elements))

    print vicon, vins
    return vicon, vins

def get_rotation(vicon, vins):
    vicon_rot_mat = quaternion_matrix(vicon[3:])
    vins_rot_mat = quaternion_matrix(vins[3:])
    #print "vicon_rot_mat", vicon_rot_mat
    #print "vins_rot_mat", vins_rot_mat
    
    return vicon[:3], vins[:3], vicon_rot_mat, vins_rot_mat

def calc_w_v_trans(vicon_trans, vins_trans, vicon_rot, vins_rot):
    T_w_jackal = vicon_rot
    T_v_body = vins_rot
    #print vicon_trans, vins_trans

    for i in range(0, 3):
        T_w_jackal[i][-1] = T_w_jackal[i][-1] + vicon_trans[i]
        T_v_body[i][-1] = T_v_body[i][-1] + vins_trans[i]

    #print "T_w_jackal: ", T_w_jackal
    #print "T_v_body: ", T_v_body

    vicon_mat = np.array(T_w_jackal)
    print "vicon_mat: ", vicon_mat
    # vicon_mat = np.array([[0.109778790,   0.00380199959,  0.993948772,    2.86808719],
    #                       [0.993681178,   0.0230959281,  -0.109837580,    0.344134724],
    #                       [-0.0233737718, 0.999726024,    0.00124253239,  -1.33700164],
    #                       [0.00000000,    0.00000000,     0.00000000,     1.00000000]])
   
    vins_mat = np.array(T_v_body)
    inverse_vins = np.linalg.inv(vins_mat)
    T_w_v = np.dot(vicon_mat, inverse_vins)
    print T_w_v
    t = []
    for i in range(0, 3):
        t.append(T_w_v[i][-1])
        T_w_v[i][-1] = 0.0
    q = quaternion_from_matrix(T_w_v)
    print "q: ", q, "t: ", t
    return q, t


if __name__ == '__main__':
    #vicon_mat , vins_mat = average_pose()
    vicon_mat, vins_mat = average_pose_slerp()
    vicon_trans, vins_trans, vicon_rot, vins_rot = get_rotation(vicon_mat, vins_mat)
    calc_w_v_trans(vicon_trans, vins_trans, vicon_rot, vins_rot)


    



