function [dice_coef] = NiftiDiceSorensen(mr_mask, ct_mask)
%NIFTIDICESORENSEN Calculates Sorensen-Dice similiarity metric
% from two nifti files 
threshold = 100;

mr_mask_V = niftiread(mr_mask);
ct_mask_V = niftiread(mr_mask);

mr_mask_V = mr_mask_V > threshold;
ct_mask_V = ct_mask_V > threshold;

dice_coef = dice(mr_mask_V, ct_mask_V);
end

