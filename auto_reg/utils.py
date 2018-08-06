#!/usr/bin/env python

import ruamel.yaml
import scipy.io
import numpy as np
import os
import nibabel as nib
from datetime import datetime
import csv

def dict_numpy2list(numpydict):
    new_dict = {}
    for k, v in numpydict.iteritems():
        new_dict[k] = v.tolist()
    return new_dict

def save_fcsv(fcsv_file,xfm_file, mat, rmv = True):
    content = load_fcsv2list(fcsv_file)
    outbasename = os.path.splitext(xfm_file)[0]
    for i in range(3, len(content)):
            content[i][1:4]=mat[i-3].astype(np.str)[0:3]
    with open(outbasename+'.fcsv','wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in content:
            writer.writerow(row)
    if rmv == True:
        os.remove(xfm_file)
    return outbasename+'.fcsv'

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

def spm_mat_to_ascii_mat(spm_mat_filename, out_filename):
    rmat = scipy.io.loadmat(spm_mat_filename)['M']
    np.savetxt(out_filename,np.linalg.inv(rmat))
    
def apply_spm(elecs_file,reorient_file):
    elec_mat = fcsv2mat(elecs_file)
    transform_name = os.path.basename(os.path.splitext(reorient_file)[0])
    rmat = scipy.io.loadmat(reorient_file)['M']
    #elec_mat = np.diag([1,-1,1]).dot(elec_mat.T).T
    elecs_reoriented = nib.affines.apply_affine(np.linalg.inv(rmat),elec_mat)
    #elecs_reoriented = np.diag([1,-1,1]).dot(elecs_reoriented.T).T
    xfm_file=os.path.splitext(elecs_file)[0]+'_xfm_spm'+'.csv'
    np.savetxt(xfm_file, elecs_reoriented, delimiter=",")
    save_fcsv(elecs_file, xfm_file, elecs_reoriented)
    print(str(elecs_reoriented))

def csv2mat(filename, fromLPS=False, cut_first=True):
    basename = os.path.splitext(filename)[0]
    mat = np.loadtxt(open(filename, "rb"), delimiter=",")
    if fromLPS:
        M = np.diag([-1,-1,1])
        mat = M.dot(mat.T).T
    if cut_first:
        mat = mat[1:]
    return mat

def txt2mat(filename):
    basename = os.path.splitext(filename)[0]
    try:
        mat = np.loadtxt(open(filename, "rb"), delimiter=" ")
    except:
        mat = np.loadtxt(open(filename, "rb"), delimiter="  ")
    return mat

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

def to_hu(n1_img, filename, threshold = [0, 100]):
    data = n1_img.get_data()
    data = data * n1_img.dataobj.slope + n1_img.dataobj.inter
    mask1 = data > threshold[1]
    mask2 = data < threshold[0]
    mask_all = np.ma.mask_or(mask1, mask2)
    data[mask_all] = 0
    new_img = resave_data(n1_img, data)
    nib.save(new_img, filename)
