#!/usr/bin/env python

import ruamel.yaml
import scipy.io
import numpy as np
import os
import nibabel as nib
from datetime import datetime


def load_elecmatrix(filename):
    mat = scipy.io.loadmat(filename)
    return mat['elecmatrix']

def save_elecmatrix(filename, mat):
    scipy.io.savemat(filename, {'__globals__':[], '__header__':'MATLAB 5.0 MAT-file Platform: posix, Created on: '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                                '__version__':'1.0', 'elecmatrix': mat})

def apply_spm(elecs_file,reorient_file):
    elec = load_elecmatrix(elecs_file)
    rmat = scipy.io.loadmat(reorient_file)['M']
    elecs_reoriented = nib.affines.apply_affine(rmat,elec)
    reoriented_elecs_file = os.path.splitext(elecs_file)[0]+'_reoriented.mat'
    scipy.io.savemat(reoriented_elecs_file, {'elecmatrix':elecs_reoriented})

def csv2mat(filename):
    basename = os.path.splitext(filename)[0]
    mat = np.loadtxt(open(filename, "rb"), delimiter=",")
    save_elecmatrix(basename+'.mat', mat)

def txt2mat(filename):
    basename = os.path.splitext(filename)[0]
    mat = np.loadtxt(open(filename, "rb"), delimiter=" ")
    save_elecmatrix(basename+'.mat',mat)

def mat2csv(filename):
    basename = os.path.splitext(filename)[0]
    mat = load_elecmatrix(filename)
    np.savetxt(basename+'.csv', mat, delimiter=",")
    return basename+'.csv'

def mat2txt(filename):
    basename = os.path.splitext(filename)[0]
    mat = load_elecmatrix(filename)
    np.savetxt(basename+'.txt', mat, delimiter=" ")
    return basename
    
def get_params(filename):
    with open(filename, 'r') as _f:
        return ruamel.yaml.round_trip_load(_f.read(), preserve_quotes=True)
    
def set_params(filename, params):
    with open(filename, 'w') as _f:
        _f.write(ruamel.yaml.dump(params, Dumper=ruamel.yaml.RoundTripDumper, width=1024))

def load_file(nii_filename):
    n1_img = nib.load(nii_filename)
    return n1_img
