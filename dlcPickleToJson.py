#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
:Description: DLC results converter from pickle to JSON

:Authors: (c) Artem Lutov <lua@lutan.ch>
:Date: 2020-08-17
"""
import os
import pickle
import json
import ruamel
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from glob import iglob
from easydict import EasyDict


class NumpyDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyDataEncoder, self).default(obj)


if __name__ == '__main__':
	parser = ArgumentParser(description='DLC results converter from pickle to JSON.',
		formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
	parser.add_argument("-d", "--outp-dir", default=None,
		help='Output directory for the converted files. The input directory is used by default.')
	parser.add_argument('input', metavar='INPUT', nargs='+',
		help='Wildcards of input files in the Python Pickle format to be converted')
	args = parser.parse_args()

	# Prepare output directory
	if args.outp_dir and not os.path.exists(args.outp_dir):
		os.makedirs(args.outp_dir)

	nfiles = 0
	for wlc in args.input:
		for ifname in iglob(wlc):
			nfiles += 1
			print('Converting {} ...'.format(ifname))
			with open(ifname, 'rb') as finp:
				data = pickle.load(finp)
				ofname = os.path.splitext(ifname)[0] + '.json'
				if args.outp_dir:
					ofname = os.path.join(args.outp_dir, os.path.split(ofname)[1])
				with open(ofname, 'w') as fout:
					json.dump(data, fout, cls=NumpyDataEncoder)
				print('  converted to:' + ofname)
