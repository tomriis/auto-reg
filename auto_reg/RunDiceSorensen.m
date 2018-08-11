function [coefs]= RunDiceSorensen(subjects, mask)
methods=["ants";"rbspline";"flirt";"rspm"];
nSubjects = length(subjects);
nMethods = length(methods);
coefs = zeros(nSubjects,nMethods);
for i = 1:nSubjects
    for j = 1:nMethods
        ct_mask = fullfile(subjects(i),"masks",strcat(methods(j),"_CT_skull_mask1500.nii.gz"));
        mr_mask = fullfile(subjects(i),"masks",mask);
        disp(ct_mask)
        disp(mr_mask)
        disp("____________________________________________")
        coefs(i, j) = NiftiDiceSorensen(mr_mask, ct_mask);
    end
end