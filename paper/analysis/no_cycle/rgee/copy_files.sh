find ~/sshfs/vic-staging/dacron/chemical_reactions/new_ff/no_water/p0_no_cycles/ -iregex .*gmx_[0-9]+_ee_rg.csv -exec cp -v {} no_cycle/ \;
find ~/sshfs/vic-staging/dacron/chemical_reactions/new_ff/no_water/scan_p0_1000/ -iregex .*gmx_[0-9]+_ee_rg.csv -exec cp -v {} cycle/ \;
