
from .utils import get_params
import subprocess
import shlex

try:
    import matlab.engine
    eng = matlab.engine.start_matlab()
except:
    print("Please set up Python Matlab Engine to use SPM")

try:
    import img_pipe
except:
    print("Please make sure you actiated the img_pipe conda environment")



class Platform:
    def __init__(self):
        self.p = {}
        self.params_file = ''
    def update_params(self):
        self.p = get_params(self.params_file)

class Fsl(Platform):
    callstring = 'bash fsl/fsl_functions.sh'
    def __init__(self):
        super().__init__(self)
        self.params_file = 'fsl/fsl_params.yml'  
        self.p = get_params(self.params_file)
    def bet(self):
        opts=[Fsl.callstring,'execute_bet',self.p['bet_input'],self.p['bet_output'], self.p['f'],self.p['g']]
        subprocess.call(opts)
    def fast(self):
        opts=[Fsl.callstring,'execute_fast', self.p['t'],self.p['n'],self.p['H'],self.p['I'],self.p['l'],self.p['fast_output_base'],self.p['fast_input']]
        subprocess.call(opts)
    def flirt(self):
        opts=[Fsl.callstring,'execute_flirt', self.p['flirt_in'], self.p['flirt_ref'], self.p['out'], self.p['omat'],self.p['bins'],self.p['cost'],self.p['searchrx'],self.p['searchry'],self.p['searchrz'],self.p['dof'],self.p['interp']]
        subprocess.call(opts)
    def fnirt(self):
        opts=[Fsl.callstring, 'execute_fnirt', self.p['fnirt_ref'], self.p['fnirt_ref']]
        subprocess.call(opts)

class Ants(Platform):
    callstring = 'bash ants/ants_functions.sh'
    def __init__(self):
        super().__init__(self)
        self.params_file = 'ants/ants_params.yml'
        self.p = get_params(self.params_file)
    def antsRegistrationSynQuick(self):
        opts=[Ants.callstring,'execute_antsRegistrationSyNQuick', self.p['fixed'],self.p['moving'], self.p['t'],self.p['o']]
        subprocess.call(opts)
        
class SPM(Platform):
	callstring = ''
	def __init__(self):
		super().__init__(self):
        self.params_file = 'spm/spm_params.yml'
        self.p = get_params(self.params_file)
    def coregister_estimate_reslice(self):
        eng.coregister_estimate_reslice(self.p['ref_img'],self.p['source_img'])
	def spm_D(self):
		eng.spm_D()


class Freesurfer(Platform):
    def __init__(self, subj, hem):
        super().__init__(self):
        self.patient = img_pipe.freeCoG(subj=subj, hem = hem)



        
