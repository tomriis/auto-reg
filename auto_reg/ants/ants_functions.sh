#!/usr/bin/env bash


function execute_antsRegistrationSyNQuick(){
    echo $(antsRegistrationSyNQuick.sh -d 3 -f $1 -m $2 -t $3 -o $4)
}

function apply_antsApplyTransfrom(){
    echo $(antsApplyTransform -d $1 -i $2 -r $3 -o $4 -t $5)
}

function apply_antsApplyTransformsToPoints(){
    echo $(antsApplyTransformsToPoints -d $1 -i $2 -o $3 -t $4)
}


"$@"
