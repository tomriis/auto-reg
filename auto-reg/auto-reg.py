#auto-reg.py
""" User interface for running all software pipelines on two files"""
import Tkinter
from Tkconstants import *
tk = Tkinter.Tk()

import platforms
import img_pipe
import utils

class Pipeline(object):
    def __init__(self,subj):
        self.subj = subj
        self.patient = img_pipe.freeCoG(subj=self.subj, hem = 'stereo')
    def preprocess(self):
        self.patient.prep_recon()
        self.patient.get_recon()
        self.patient.convert_fsmesh2mlab()
        self.patient.get_subcort()

    def coregister(self, methods = []):
        if len(methods) == 0:
            methods = ['ants','spm','fsl','img_pipe']
        for method in methods:
            

    def evaluate(self):
