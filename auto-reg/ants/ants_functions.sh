#!/usr/bin/env bash


function execute_antsRegistrationSyNQuick(){
    echo $(antsRegistrationSyNQuick.sh -d 3 -f $1 -m $2 -t $3 -o $4)
}

"$@"
