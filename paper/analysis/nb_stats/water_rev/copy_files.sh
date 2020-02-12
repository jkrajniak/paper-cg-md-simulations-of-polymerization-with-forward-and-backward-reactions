#! /bin/sh
#
# copy_files.sh
# Copyright (C) 2017 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

DIR=dacron/chemical_reactions/new_ff/with_water_rev/scan_k1_new_wgh/data

find ~/sshfs/vic-staging/${DIR} -name "nb_A_DE_pp_*" | while read a; do cp -v $a .; done
find ~/sshfs/vic-staging/${DIR} -name "pp_*energy*" | while read a; do cp -v $a .; done
