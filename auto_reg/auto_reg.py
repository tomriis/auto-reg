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
                print("Ran SPM--BOOM!")
    def apply_xfms2elecs(self):
        elecs_files = glob.glob(self.patient.elecs_dir+'/individual_elecs/*.mat')
        for elec in elecs_files:
            outbasename = os.path.splitext(elec)[0][0]
            self.platforms['ants'].antsApplyTransformsToPoints(utils.mat2csv(elec),outbasename+'AntsXFM.csv', self.coreg_out) #TODO find what transform needs to be applied!
        
    def evaluate(self):
        print('flim')
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
    def set_directory_structure(self):
        for method in self.platforms.keys():
            if not os.path.exists(self.coreg_out[method]):
                os.makedirs(self.coreg_out[method])

class Metrics(object):
    def __init__(self):
        pass
        
