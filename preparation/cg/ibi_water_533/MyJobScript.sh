#!/bin/bash -l
#PBS -N MELF_NPT_468
#PBS -l walltime=24:00:00
#PBS -o Output.job
#PBS -j oe
#PBS -l nodes=1:ppn=20
#PBS -M jakub.krajniak@cs.kuleuven.be
#PBS -A  lp_sim_interpoco

source switch_to_2015a

module purge
module load 2015a/votca/1.5-devel

module load 2015a/GROMACS/2016.3

MDRUN="mdrun_mpi"
GROMPP="grompp_mpi"

cd $PBS_O_WORKDIR

# Set up OpenMPI environment
n_proc=$(cat $PBS_NODEFILE | wc -l)
n_node=$(cat $PBS_NODEFILE | uniq | wc -l)

csg_inverse --options settings.xml
