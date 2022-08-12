export path_to_install=$(realpath $(dirname -- "$0")/install)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$path_to_install/lib64 # or lib based on your architecture
export PYTHONPATH=$PYTHONPATH:$path_to_install/lib64 # or lib based on your architecture
