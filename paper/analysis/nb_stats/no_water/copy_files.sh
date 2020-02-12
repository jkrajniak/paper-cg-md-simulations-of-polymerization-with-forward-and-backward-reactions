#! /bin/sh
#
# copy_files.sh
# Copyright (C) 2017 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

DIR=dacron/chemical_reactions/new_ff/no_water/scan_p0_1000/data

find ~/sshfs/vic-staging/${DIR} -name "nb_A_DE_p_*" | while read a; do cp -v $a .; done
find ~/sshfs/vic-staging/${DIR} -name "p_0.001*energy*" | while read a; do cp -v $a .; done
