% List of open inputs
% Coregister: Estimate & Reslice: Reference Image - cfg_files
% Coregister: Estimate & Reslice: Source Image - cfg_files
function coregister_estimate_reslice(ref_img, source_img)
    jobfile = {'C:\Users\Tom\Documents\MATLAB\coregister_estimate_reslice_job.m'};
    jobs = repmat(jobfile, 1, 1);
    inputs = cell(2, 1);
    inputs{1, 1} = ref_img; % Coregister: Estimate & Reslice: Reference Image - cfg_files
    inputs{2, 1} = source_img; % Coregister: Estimate & Reslice: Source Image - cfg_files
    spm('defaults', 'FMRI');
    spm_jobman('run', jobs, inputs{:});
end
