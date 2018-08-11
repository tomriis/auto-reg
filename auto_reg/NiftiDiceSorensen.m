function [dice_coef] = NiftiDiceSorensen(mr_mask, ct_mask)
%NIFTIDICESORENSEN Calculates Sorensen-Dice similiarity metric
% from two nifti files 
ct_threshold = 250;
mr_threshold = 0.5;

mr_mask_V = niftiread(mr_mask);
ct_mask_V = niftiread(ct_mask);

mr_mask_V = mr_mask_V > mr_threshold;
ct_mask_V = ct_mask_V > ct_threshold;

dice_coef = dice(mr_mask_V, ct_mask_V);
end

