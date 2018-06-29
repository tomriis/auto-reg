#!/usr/bin/env bash

function execute_bet() {
    echo $(bet $1 $2 -f $3 -g $4)
}

function execute_fast(){
    echo $(fast -t $1 -n $2 -H $3 -I $4 -l $5 -o $6 $7)
}

function execute_flirt(){
    echo $(flirt -in $1 -ref $2 -out $3 -omat $4 -bins $5 -cost $6 -searchrx $7 -searchry $8 -searchrz $9 -dof ${10} -interp ${11})
}

function apply_flirt(){
    echo $(flirt -in $1 -ref $2 -out $3 --init $4 -applyxfm)
}

function execute_fnirt(){
    echo $(fnirt --ref=$1 --in=$2 --cout=$3)
}

function apply_fnirt(){
    echo $(applywarp --ref=$1 --in=$2 --warp=$3 --out=$4)
}

"$@"

