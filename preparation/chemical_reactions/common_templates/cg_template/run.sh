MD="em.mdp nvt.mdp" # nvt1.mdp"
FIRST=1
LASTDIR=""

for mdp in $MD; do
    workdir=`basename $mdp .mdp`
    if [ -d "$workdir" ]; then
        LASTDIR=$workdir
        FIRST=0
        continue
    fi
    mkdir $workdir
    if [ "$FIRST" == "1" ]; then
        cp -v conf.gro $workdir
        FIRST=0
    else
        cp -v $LASTDIR/confout.gro $workdir/conf.gro
    fi
    cp $mdp $workdir
    cp topol.top $workdir
    cp index.ndx $workdir
    cd $workdir
    for f in ../*.xvg; do
        ln -s $f `basename $f`
    done
    gmx_mpi grompp -f $mdp -v -n && mpirun -n $n_proc gmx_mpi mdrun -v -tableb table_*
    LASTDIR=$workdir
    cd ..
done
