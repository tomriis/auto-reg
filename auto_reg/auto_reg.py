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
            self.flirt_xfm2elecs(elec)
            self.fnirt_xfm2elecs(elec)
            self.ants_xfm2elecs(elec)
            self.spm_xfm2elecs(elec)
            
    def flirt_xfm2elecs(self, elec):
        outbasename = os.path.splitext(elec)[0]
        fmat = fcsv2mat(elec)
        fsl_source = utils.elecs2txt(elec, mat = fmat)
        self.platforms['fsl'].apply_flirt2coords(fsl_source, self.patient.CT, self.coreg_out['fsl']+'/flirt_out.nii', self.flirt_omat, outbasename+'_flirt_xfm.txt')
        utils.txt2elecs(outbasename+'_flirt_xfm.txt')
        
    def fnirt_xfm2elecs(self, elec):
        outbasename = os.path.splitext(elec)[0]
        fmat = fcsv2mat(elec)
        fsl_source = utils.elecs2txt(elec,mat=fmat)
        self.platforms['fsl'].apply_fnirt2coords(fsl_source, self.patient.CT, self.patient.T1, self.fnirt_warp, outbasename+'_fnirt_xfm.txt')
        utils.txt2elecs(outbasename+'_fnirt_xfm.txt')
        
    def ants_xfm2elecs(self, elec, RAS=True):
        outbasename = os.path.splitext(elec)[0]
        fmat = fcsv2mat(elec)
        ants_source = utils.elecs2csv(elec, toLPS=RAS, mat = fmat)
        self.platforms['ants'].antsApplyTransformsToPoints(ants_source, outbasename+'_ants_xfm.csv', self.ants_invwarp, self.ants_mat)
        utils.csv2elecs(outbasename+'_ants_xfm.csv', fromLPS=RAS)

    def spm_xfm2elecs(self, elec, reorient_file = None):
        if reorient_file == None:
            reorient_file = self.coreg_out['spm']+'/matrix.mat'
        utils.apply_spm(elec, reorient_file)
        
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
        self.platforms['spm'].p['output_dir']=os.path.join(self.patient.patient_dir,'/acpc/')
    def set_directory_structure(self):
        for method in self.platforms.keys():
            if not os.path.exists(self.coreg_out[method]):
                os.makedirs(self.coreg_out[method])

class Metrics(object):
    def __init__(self):
        pass
        
