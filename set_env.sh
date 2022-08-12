source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/setup.sh
export path_to_install=$(realpath $(dirname -- "$0")/install)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$path_to_install/lib64 # or lib based on your architecture
export PYTHONPATH=$PYTHONPATH:$path_to_install/lib64 # or lib based on your architecture
