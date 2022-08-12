# dual-readout_TB

FWcore for TB data analysis

## Dependencies
* ROOT 6.26/04
* python 3.9.12
* boost::python

## Compile

```sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_102/x86_64-centos7-gcc11-opt/setup.sh # on lxplus for dependencies
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install -j4
```

## Environment setup

```sh
source set_env.sh
```
or
```sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<path_to_install>/lib64 # or lib based on your architecture
export PYTHONPATH=$PYTHONPATH:<path_to_install>/lib64 # or lib based on your architecture
```
