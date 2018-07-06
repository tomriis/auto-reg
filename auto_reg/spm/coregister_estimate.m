function coregister_estimate(ref, input,output_dir)
    VG = spm_vol(ref);
    VF = spm_vol(input);
    X = spm_coreg(VG, VF);
    matrix= spm_matrix(X(:)');
    VG2VF = VF.mat\matrix*VG.mat;
    VF2VG = inv(VG2VF);
    M = matrix;
    save(fullfile(output_dir,'matrix.mat'),'M');
    M = VG2VF;
    save(fullfile(output_dir,'VG2VF.mat'), 'M');
    M = VF2VG;
    save(fullfile(output_dir,'VF2VG.mat'), 'M');
end