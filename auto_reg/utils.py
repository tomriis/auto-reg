#!/usr/bin/env python

import ruamel.yaml
import scipy.io
import numpy as np
import os
import nibabel as nib
from datetime import datetime
import csv

def save_fcsv(filename, mat):

def load_fcsv2list(filename):
    content = []
    with open(filename,'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            content.append(row)
    return content

def fcsv2mat(filename):
    content = load_fcsv2list(filename)
    mat = []
    for i in range(3,len(content)):
        mat.append(np.array(content[i][1:4]).astype(np.float))
    return np.vstack(mat)

def load_elecmatrix(filename):
    mat = scipy.io.loadmat(filename)
    return mat['elecmatrix']

def save_elecmatrix(filename, mat):
    scipy.io.savemat(filename, {'__globals__':[], '__header__':'MATLAB 5.0 MAT-file Platform: posix, Created on: '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                                '__version__':'1.0', 'elecmatrix': mat})
def mm2vox(filename, nii):
    if isinstance(nii, str):
        nii = load_file(nii)
    mat = load_elecmatrix(filename)
    inv = np.linalg.inv(nii.affine)
    vox_coords = nib.affines.apply_affine(inv,mat)
    out_filename = os.path.splitext(filename)[0]+'_vox.mat'
    save_elecmatrix(out_filename, vox_coords)
    return out_filename

def vox2mm(filename, nii):
    if isinstance(nii, str):
        nii = load_file(nii)
    mat = load_elecmatrix(filename)
    mm_coords = nib.affines.apply_affine(nii.affine,mat)
    out_filename = os.path.splitext(filename)[0]+'_mm.mat'
    save_elecmatrix(out_filename, mm_coords)
    return out_filename
    
    
def apply_spm(elecs_file,reorient_file):
    elec = load_elecmatrix(elecs_file)
    transform_name = os.path.basename(os.path.splitext(reorient_file)[0])
    rmat = scipy.io.loadmat(reorient_file)['M']
    elecs_reoriented = nib.affines.apply_affine(rmat,elec)
    np.savetxt(os.path.splitext(elecs_file)[0]+'_spm'+'.csv', elecs_reoriented, delimiter=",")
    reoriented_elecs_file = os.path.splitext(elecs_file)[0]+'_spm_'+transform_name+'.mat'
    save_elecmatrix(reoriented_elecs_file, elecs_reoriented)

def csv2elecs(filename, fromLPS=False):
    basename = os.path.splitext(filename)[0]
    mat = np.loadtxt(open(filename, "rb"), delimiter=",")
    if fromLPS:
        M = np.diag([-1,-1,1])
        mat = M.dot(mat.T).T
    save_fcsv(basename+'.fcsv', mat)

def txt2elecs(filename):
    basename = os.path.splitext(filename)[0]
    try:
        mat = np.loadtxt(open(filename, "rb"), delimiter=" ")
    except:
        mat = np.loadtxt(open(filename, "rb"), delimiter="  ")
        
    save_fcsv(basename+'.fcsv',mat)

def elecs2csv(filename, toLPS = False, mat = False):
    basename = os.path.splitext(filename)[0]
    try:
        mat.shape
    except:
        mat = load_elecmatrix(filename)
    if toLPS:
        M = np.diag([-1,-1,1])
        mat = M.dot(mat.T).T
    mat = np.vstack((np.array([0,0,0]), mat))
    np.savetxt(basename+'.csv', mat, delimiter=",")
    return basename+'.csv'

def elecs2txt(filename, mat = False):
    basename = os.path.splitext(filename)[0]
    try:
        mat.shape
    except:
        mat = load_elecmatrix(filename)
    np.savetxt(basename+'.txt', mat, delimiter=" ")
    return basename+'.txt'
    
def get_params(filename):
    with open(filename, 'r') as _f:
        return ruamel.yaml.round_trip_load(_f.read(), preserve_quotes=True)
    
def set_params(filename, params):
    with open(filename, 'w') as _f:
        _f.write(ruamel.yaml.dump(params, Dumper=ruamel.yaml.RoundTripDumper, width=1024))

def load_file(nii_filename):
    n1_img = nib.load(nii_filename)
    return n1_img

def resave_data(nifti_orig, data):
    hdr = nifti_orig.header.copy()
    new_img = nib.nifti1.Nifti1Image(data, None, header = hdr)
    return new_img
