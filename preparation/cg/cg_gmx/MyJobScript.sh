#!/bin/bash 
#PBS -N PE_CG_423
#PBS -l mem=16gb
#PBS -l walltime=24:00:00
#PBS -o Output.job
#PBS -j oe
#PBS -l nodes=1:ppn=20
#PBS -M jakub.krajniak@kuleuven.be
#PBS -A lp_polymer_goa_project

module purge
module load GROMACS

cd $PBS_O_WORKDIR

# Set up OpenMPI environment
n_proc=$(cat $PBS_NODEFILE | wc -l)
n_node=$(cat $PBS_NODEFILE | uniq | wc -l)
mpdboot -f $PBS_NODEFILE -n $n_node -r ssh -v

grompp_mpi -v -n

mpiexec -n $n_proc mdrun_mpi -v

mpdallexit
