#!/bin/bash -l
#PBS -N DIOL  
#PBS -l mem=8gb
#PBS -l walltime=1:00:00
#PBS -o Output.job
#PBS -j oe
#PBS -l nodes=1:ppn=20
module load GROMACS/5.0.5-intel-2015a-hybrid

cd $PBS_O_WORKDIR

gmx_mpi mdrun -v -ntomp 20 
