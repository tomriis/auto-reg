
from .utils import get_params
import subprocess
import shlex


class Fsl():
    callstring = 'bash fsl/fsl_functions.sh'
    params_file = 'fsl/fsl_params.yml'
    def __init__(self):
        self.p = get_params(Fsl.params_file)
    def bet(self):
        opts=[Fsl.callstring,self.p['bet_input'],self.p['bet_output'], self.p['f'],self.p['g']]
        subprocess.call(opts)
    def fast(self):
        opts=[Fsl.callstring, self.p['t'],self.p['n'],self.p['H'],self.p['I'],self.p['l'],self.p['fast_output_base'],self.p['fast_input']]
        subprocess.call(opts)
    def flirt(self):
        opts=[Fsl.callstring, self.p['flirt_in'], self.p['flirt_ref'], self.p['out'], self.p['omat'],self.p['bins'],self.p['cost'],self.p['searchrx'],self.p['searchry'],self.p['searchrz'],self.p['dof'],self.p['interp']]
        subprocess.call(opts)
            
