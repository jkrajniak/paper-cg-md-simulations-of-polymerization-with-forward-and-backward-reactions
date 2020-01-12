d=`pwd`
for f in data/p_0.001_*0.95*.h5; do
    outdir=gmx_`basename $f | cut -f3 -d_`
    basename=`basename $f _traj.h5`
    mkdir -v $outdir
    python ../../common_code/convert_cg_topol.py --top data/${basename}_output_topol.top --h5 data/${basename}_traj.h5 --conf data/${basename}_confout.gro --out_top $outdir/topol.top --out_conf $outdir/conf.gro
    cp -v cg_template/* $outdir/
    echo -e "a A*\n a B*\n a Q*\n a D*\n a E*\n q\n" | gmx_mpi make_ndx -f $outdir/conf.gro -o $outdir/index.ndx
    sed -i 's/\*//g; s/Q/C/g' $outdir/index.ndx
done
