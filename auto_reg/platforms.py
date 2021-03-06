
import utils
import subprocess

try:
    import matlab.engine
    eng = matlab.engine.start_matlab()
except:
    print("Please set up Python Matlab Engine to use SPM")

class Platform(object):
    def __init__(self):
        self.p = {}
        self.params_file = ''
    def update_params(self):
        self.p = utils.get_params(self.params_file)
    def set_params(self):
        utils.set_params(self.params_file, self.p)
        self.p = utils.get_params(self.params_file)
        

class Fsl(Platform):
    callstring = 'fsl/fsl_functions.sh'
    def __init__(self):
        super(Fsl, self).__init__()
        self.params_file = 'fsl/fsl_params.yml'  
        self.p = utils.get_params(self.params_file)
    def bet(self):
        opts=['bash',Fsl.callstring,'execute_bet',self.p['bet_input'],self.p['bet_output'], str(self.p['f']),str(self.p['g'])]
        subprocess.call(opts)
    def fast(self):
        opts=['bash',Fsl.callstring,'execute_fast', str(self.p['t']),str(self.p['n']),str(self.p['H']),str(self.p['I']),str(self.p['l']),self.p['fast_output_base'],self.p['fast_input']]
        subprocess.call(opts)
    def flirt(self):
        opts=['bash',Fsl.callstring,'execute_flirt', self.p['input'], self.p['ref'], self.p['out'], self.p['omat'],str(self.p['bins']),self.p['cost'],self.p['searchrx'],self.p['searchry'],self.p['searchrz'],str(self.p['dof']),self.p['interp']]
        subprocess.call(opts)
    def fnirt(self):
        opts=['bash',Fsl.callstring, 'execute_fnirt', self.p['ref'], self.p['input'],self.p['aff'], self.p['cout'], self.p['iout']]
        subprocess.call(opts)
    def apply_flirt(self, invol, refvol, invol2refvolmat, out):
        opts=['bash',Fsl.callstring, 'apply_flirt',invol,refvol,out, invol2refvolmat]
        subprocess.call(opts)
    def apply_fnirt(self, invol, refvol, warp, out):
        opts = ['bash',Fsl.callstring, 'apply_fnirt',refvol,invol,warp,out]
        subprocess.call(opts)
    def apply_flirt2coords(self,coordfile, src, dest, xfm, outfile):
        opts = ['bash',Fsl.callstring, 'apply_flirt2coords',coordfile, src, dest, xfm, outfile]
        subprocess.call(opts)
    def apply_fnirt2coords(self,coordfile, src, dest, warp, outfile):
        opts = ['bash',Fsl.callstring, 'apply_fnirt2coords',coordfile, src,dest,warp, outfile]
        subprocess.call(opts)


class Ants(Platform):
    callstring = 'ants/ants_functions.sh'
    def __init__(self):
        super(Ants, self).__init__()
        self.params_file = 'ants/ants_params.yml'
        self.p = utils.get_params(self.params_file)
    def antsRegistrationSynQuick(self):
        opts=['bash',Ants.callstring,'execute_antsRegistrationSyNQuick', self.p['fixed'],self.p['moving'], self.p['t'],self.p['o']]
        subprocess.call(opts)
    def antsApplyTransforms(self,in_img, ref,warp, mat,out, img_dim=3):
        opts=['bash',Ants.callstring,'apply_antsApplyTransforms',str(img_dim), in_img,ref, warp, mat, out]
        subprocess.call(opts)
    def antsApplyTransformsToPoints(self, in_csv, out_csv, warp, mat, img_dim=3):
        opts=['bash',Ants.callstring,'apply_antsApplyTransformsToPoints',str(img_dim), in_csv, out_csv, warp, mat]
        subprocess.call(opts)
        
class SPM(Platform):
    callstring = ''
    def __init__(self):
	super(SPM, self).__init__()
        self.params_file = 'spm/spm_params.yml'
        self.p = utils.get_params(self.params_file)
    def coregister_estimate(self):
        eng.coregister_estimate(self.p['ref_img'],self.p['source_img'], self.p['output_dir'])
    def coregister_estimate_vol(self, ref_file, in_file):
    	eng.coreg_estimate_vol(ref_file, in_file)
    def spm_D(self):
		eng.spm_D()

        
