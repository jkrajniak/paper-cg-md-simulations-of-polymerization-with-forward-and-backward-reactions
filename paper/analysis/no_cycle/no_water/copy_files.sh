#! /bin/sh
#
# copy_files.sh
# Copyright (C) 2017 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

DIR=dacron/chemical_reactions/new_ff/no_water/p0_no_cycles/data

find ~/sshfs/vic-staging/${DIR} -name "state*p_0.001*" | while read a; do cp -v $a .; done
find ~/sshfs/vic-staging/${DIR} -name "polstat_p_0.001*" | while read a; do cp -v $a .; done
