# `mosaic` examples

This repo contains example scripts using `mosaic` to visualize MPAS
data on its native mesh in `matplotlib`. This repo assumes you are a
member of the `e3sm` unix group on `perlmutter` in order to read in the
mesh and data files. The only other requirement is a `python` environment
with `mosaic` available. The easiest option would be to load the latest
version of `e3sm_unified`: 
```shell
source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_pm-cpu.sh
```

To render the example figure, run:
```shell
make
```
or run the example script (in `src/`) of your choice from the command line
or from a python interpreter (e.g. `ipython`) . 

## Example notebook
If you'd like to run the example notebook, you will need to make the `e3sm_unified`
environment a python kernel to use it in a jupyter notebook at NERSC 
(see [here](https://docs.nersc.gov/services/jupyter/how-to-guides/#how-to-use-a-conda-environment-as-a-python-kernel)). 
Assuming the `e3sm_unified_1.11.1` environment is already loaded, just run: 
```shell
python -m ipykernel install --user --name e3sm_unified_1.11.1 --display-name e3sm_unified_1.11.1
```
and then go to https://jupyter.nersc.gov/. 

## Performance profiling
To run the performance profiling yourself, you can run:
```shell
make profile N=10
```
where you can set `N` to the number of iterations you'd like.

