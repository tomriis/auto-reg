#!/usr/bin/env bash

function execute_bet() {
    bet $1 $2 -f $3 -g $4
}

function execute_fast(){
    fast -t $1 -n $2 -H $3 -I $4 -l $5 -o $6 $7
}



