#auto_reg.py
""" User interface for running all software pipelines on two files"""
import os
import glob
#import Tkinter
#from Tkconstants import *
#tk = Tkinter.Tk()

import platforms
import img_pipe
import utils
import numpy as np

class Pipeline(object):
    def __init__(self,subj):
        self.subj = subj
        self.patient = img_pipe.freeCoG(subj=self.subj, hem = 'stereo')
        self.patient.CT = os.path.join(self.patient.CT_dir, 'CT.nii')
        self.patient.T1 = os.path.join(self.patient.acpc_dir, 'T1.nii')
        
        self.platforms ={'fsl': platforms.Fsl(),
                         'ants':platforms.Ants(),
                         'spm':platforms.SPM()}

        self.coreg_out = {'fsl':os.path.join(self.patient.patient_dir,'coreg_fsl'),
                          'ants': os.path.join(self.patient.patient_dir, 'coreg_ants'),
                          'spm':os.path.join(self.patient.patient_dir, 'coreg_spm')}
        
        self.update_param_files()
        self.set_directory_structure()

        self.ants_warp = os.path.join(self.coreg_out['ants'],'ants_1Warp.nii.gz')
        self.ants_mat = os.path.join(self.coreg_out['ants'],'ants_0GenericAffine.mat')
        self.ants_invwarp = os.path.join(self.coreg_out['ants'],'ants_1InverseWarp.nii.gz')
        self.fnirt_warp = os.path.join(self.coreg_out['fsl'],'fnirt_cout.nii.gz')
        self.flirt_omat = os.path.join(self.coreg_out['fsl'],'flirt_omat.mat')
        
    def preprocess(self):
        self.patient.prep_recon()
        self.patient.get_recon()
        self.patient.convert_fsmesh2mlab()
        self.patient.get_subcort()

    def coregister(self, methods = []):
        if len(methods) == 0:
            methods = self.platforms.keys()
        for method in methods:
            if method == 'fsl':
                self.platforms['fsl'].flirt()
                self.platforms['fsl'].fnirt()
            elif method == 'ants':
                self.platforms['ants'].antsRegistrationSynQuick()
            elif method == 'spm':
                self.platforms['spm'].coregister_estimate()
    def apply_xfms2elecs(self):
        elecs_files = glob.glob(self.patient.elecs_dir+'/*.fcsv')   
        for elec in elecs_files:
            print("---- Processing : "+elec)
            self.flirt_xfm2elecs(elec)
            self.fnirt_xfm2elecs(elec)
            self.ants_xfm2elecs(elec)
            self.spm_xfm2elecs(elec)
            
    def flirt_xfm2elecs(self, elec):
        outbasename = os.path.splitext(elec)[0]
        xfm_file = outbasename+'_xfm_flirt.txt'
        fmat = utils.fcsv2mat(elec)
        fsl_source = utils.elecs2txt(elec, mat = fmat)
        self.platforms['fsl'].apply_flirt2coords(fsl_source, self.patient.CT, self.coreg_out['fsl']+'/flirt_out.nii', self.flirt_omat, xfm_file)
        rmat = utils.txt2mat(xfm_file)
        utils.save_fcsv(elec, xfm_file, rmat)
        
    def fnirt_xfm2elecs(self, elec):
        outbasename = os.path.splitext(elec)[0]
        xfm_file = outbasename+'_xfm_fnirt.txt'
        fmat = utils.fcsv2mat(elec)
        fsl_source = utils.elecs2txt(elec,mat=fmat)
        self.platforms['fsl'].apply_fnirt2coords(fsl_source, self.patient.CT, self.patient.T1, self.fnirt_warp, xfm_file)
        rmat = utils.txt2mat(xfm_file)
        utils.save_fcsv(elec, xfm_file, rmat)
        
    def ants_xfm2elecs(self, elec, RAS=True):
        outbasename = os.path.splitext(elec)[0]
        xfm_file = outbasename+'_xfm_ants.csv'
        fmat = utils.fcsv2mat(elec)
        ants_source = utils.elecs2csv(elec, toLPS=RAS, mat = fmat)
        self.platforms['ants'].antsApplyTransformsToPoints(ants_source, xfm_file, self.ants_invwarp, self.ants_mat)
        rmat = utils.csv2mat(xfm_file, fromLPS=RAS)
        utils.save_fcsv(elec, xfm_file, rmat)
        
    def spm_xfm2elecs(self, elec, reorient_file = None):
        if reorient_file == None:
            reorient_file = self.coreg_out['spm']+'/matrix.mat'
        utils.apply_spm(elec, reorient_file)
        
    def evaluate(self):
        elecs_files = glob.glob(self.patient.elecs_dir+'/*.fcsv')
    def update_param_files(self):
        self.update_input_files()
        self.update_ref_files()
        self.update_out_files()
        self.platforms['fsl'].set_params()
        self.platforms['ants'].set_params()
        self.platforms['spm'].set_params()
    def update_input_files(self):
        self.platforms['fsl'].p['input']=self.patient.CT        
        self.platforms['ants'].p['moving'] = self.patient.CT
        self.platforms['spm'].p['source_img'] = self.patient.CT
    def update_ref_files(self):
        self.platforms['fsl'].p['ref']=self.patient.T1
        self.platforms['ants'].p['fixed'] = self.patient.T1
        self.platforms['spm'].p['ref_img'] = self.patient.T1
    def update_out_files(self):
        self.platforms['fsl'].p['out']=self.coreg_out['fsl']+'/flirt_out'
        self.platforms['fsl'].p['omat']=self.coreg_out['fsl']+'/flirt_omat.mat'
        self.platforms['fsl'].p['cout']=self.coreg_out['fsl']+'/fnirt_cout'
        self.platforms['ants'].p['o']=self.coreg_out['ants']+'/ants_'
        self.platforms['spm'].p['output_dir']=os.path.join(self.patient.patient_dir,'/acpc/')
    def set_directory_structure(self):
        for method in self.platforms.keys():
            if not os.path.exists(self.coreg_out[method]):
                os.makedirs(self.coreg_out[method])

class Metrics(object):
    def __init__(self):
        self.xfms =  {'ants': [], 'flirt': [],'spm':[], 'fnirt': []}
        self.elecs_groups = {}
        
    def pairwise_difference(self, elecs_files):
        self.set_xfms_dict(elecs_files)
        keys = self.xfms.keys()
        pairwise_diff = {}
        for i in range(len(keys)-1):
            for j in range(i+1,len(keys)):
                dist = np.sqrt((self.xfms[keys[i]]-self.xfms[keys[j]])**2.0)
                pairwise_diff[keys[i]+'_v_'+keys[j]] = dist
        return pairwise_diff
    
    def set_xfms_dict(self, elecs_files):
        keys = self.xfms.keys()
        for key in keys:
            for elec in elecs_files:
                if key in elec:
                    self.xfms[key] = utils.fcsv2mat(elec)
    def group_by_base(self, elecs_files, basename):
        # Groups list of elec files by the number following the basename
        base = os.path.dirname(elecs_files[0])+'/'+basename
        groups = np.unique([elec[len(base):len(base)+2] for elec in elecs_files])
        for num in groups:
            self.elecs_groups[basename+num] = [f for f in elecs_files if base+num in f]
        return self.elecs_groups
    def concat_all(self, elecs_dict):
        keys = self.xfms.keys()
        diffs_all = {}
        for i in range(len(keys)-1):
            for j in range(i+1,len(keys)):
                current_pair = keys[i]+'_v_'+keys[j]
                diffs_all[current_pair] = np.array([]).reshape(0,3)
                for group in elecs_dict.keys():
                    for pair in elecs_dict[group].keys():
                        if keys[i] in pair and keys[j] in pair:
                            diffs_all[current_pair]=np.concatenate((diffs_all[current_pair], elecs_dict[group][pair]), axis = 0)
        return diffs_all
        
