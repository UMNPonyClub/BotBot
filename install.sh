#!/bin/bash

# Usage function
function usage(){
cat <<EOF
    Usage: $0 [flags]
    Flags
    -----
    -h | --help
        print help message
    -b | --base
        Base installation directory for camoco (default: ~/.camoco).
    -v | --verbose
        Turn verbosity on.
EOF
exit 0
}

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

function log(){
    if [ $VERBOSE==true ]
    then
        printf "$1"
    fi
}

function red(){
    printf "${RED}$1${NC}\n"
}
function green(){
    printf "${GREEN}$1${NC}\n"
}

# Command Line Argument Processing
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE="/home/mccuem/shared/.local"
NAME='botbot'
VERBOSE=false

while [[ $# > 0 ]]
do
key="$1"
case $key in 
    -h|--help)
    usage
    shift
    ;;
    -b|--base)
    BASE=$2
    shift
    ;;
    -v|--verbose)
    VERBOSE=true
    shirt
    ;;
    *)  
        #unknown options
    ;;
esac
shift
done

# Installation Functions


#===================================================
#----------------Install conda ---------------------
#===================================================

function setup_shared_space {
    #===================================================
    #----------Setup the build Environment--------------
    #===================================================
    echo "Setting up the build environment"
    if [ ! -f $BASE/.bashrc ]; then
        touch $BASE/.bashrc
    fi 
    source $BASE/.bashrc
    mkdir -p $BASE
    mkdir -p $BASE/conda
    mkdir -p $BASE/bin 
    mkdir -p $BASE/lib 

}

function install_conda {
    if [ ! -e $BASE/conda/bin/conda ]
    then
        green "Downloading conda"
        cd $BASE
        wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
        bash miniconda.sh -b -f -p $BASE/conda
        rm -f miniconda.sh
    elif [ $VERBOSE = true ]
    then
        green "Conda Already Installed" 
    fi
    if [ ! -d $BASE/conda/envs/$NAME ]
    then
        echo "Making the conda virtual environment named $NAME in $BASE"
        conda remove -y --name $NAME --all
        conda config --add envs_dirs $BASE/conda/envs
        conda create -y -n $NAME --no-update-deps python=3.4 setuptools pip \
            cython==0.22.1 nose six pyyaml yaml pyparsing python-dateutil pytz numpy \
            scipy pandas matplotlib==1.4.3 numexpr patsy statsmodels pytables flask \
            ipython mpmath pytest-cov psutil==3.4.2 jinja2 
        #conda remove -y -n $NAME libgfortran --force
        #conda install -y -n $NAME libgcc --force
        conda install --no-update-deps -y -n $NAME -c http://conda.anaconda.org/omnia termcolor
        conda install --no-update-deps -y -n $NAME -c http://conda.anaconda.org/cpcloud ipdb
    elif [ $VERBOSE = true ]
    then
        green 'PonyClub Virtual Environment already installed'
    fi
}


function append_shared_bashrc {
    if [ $(cat ~/.bashrc | grep "source $BASE/.bashrc" | wc -l) -ne 1 ]; then 
        echo "source $BASE/.bashrc" >> ~/.bashrc
    fi;
}


function install-inotify-wrapper {
    pip install git+git://github.com/jackstanek/PyInotify#egg=inotify-0.2.7
}

function install-requirements {
    pip install -r $SOURCE_DIR/requirements.txt
}

function install-botbot {
    pip install git+git://github.com/jackstanek/PyInotify#egg=inotify-0.2.7
    pip install -r $SOURCE_DIR/requirements.txt
    pip install -e $SOURCE_DIR
}

setup_shared_space
install_conda
