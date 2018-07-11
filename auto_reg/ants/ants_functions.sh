#!/usr/bin/env bash


function execute_antsRegistrationSyNQuick(){
    echo $(antsRegistrationSyNQuick.sh -d 3 -f $1 -m $2 -t $3 -o $4)
}

function apply_antsApplyTransforms(){
    echo $(antsApplyTransforms -d $1 -i $2 -r $3 -t $4 -t $5 -o $6)
}

function apply_antsApplyTransformsToPoints(){
    echo $(antsApplyTransformsToPoints -d $1 -i $2 -t $5 -t $4 -o $3)
}


"$@"
