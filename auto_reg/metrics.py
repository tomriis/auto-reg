# metrics.py
"""Use 3rd party and custom software to analyze registrations"""

import nibabel as nib

def load_file(nii_filename):
    n1_img = nib.load(nii_filename)
    return n1_img

