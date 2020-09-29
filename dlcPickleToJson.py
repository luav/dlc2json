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
from math import isnan
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from glob import iglob
from easydict import EasyDict


class NumpyDataEncoder(json.JSONEncoder):
	"""JSON serializer of numpy types"""
	
	nan = None  # Replacement for the NoN value with the specified floating point value
	assert nan is None or isinstance(nan, float), 'nan is invalid: ' + str(nan)
	
	#def __init__(self, nan=None):
	#	"""Replace NoN value with the specified floating point value
	#	
	#	nan: float  - substituting value
	#	"""
	#	assert nan is None or isinstance(nan, float), 'nan is invalid: ' + str(nan)
	#	self.nan = nan
	
	def default(self, obj):
		"""JSON serialization handler of numpy types"""
		if isinstance(obj, np.integer):
			return int(obj)
		elif isinstance(obj, np.floating):
			return float(obj) if self.nan is None or not isnan(obj) else self.nan
		elif isinstance(obj, np.ndarray):
			if self.nan is not None:
				# np.nan_to_num(obj, copy=False)
				obj = np.where(obj == obj, obj, obj.dtype.type(self.nan))  # Note: nan != nan
			return obj.tolist()
		elif self.nan is not None and isinstance(obj, float):
			obj = self.nan
		return super(NumpyDataEncoder, self).default(obj)


if __name__ == '__main__':
	parser = ArgumentParser(description='DLC results converter from pickle to JSON.',
		formatter_class=ArgumentDefaultsHelpFormatter, conflict_handler='resolve')
	parser.add_argument("-d", "--outp-dir", default=None,
		help='Output directory for the converted files. The input directory is used by default.')
	parser.add_argument("--nan-value", default=None,
		help='Prohibit NaN value to be strictly compliant with the JSON format by replacing NaN with the specified floating point value.')
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
					NumpyDataEncoder.nan = args.nan_value
					json.dump(data, fout, cls=NumpyDataEncoder, allow_nan=args.nan_value is None)
				print('  converted to:' + ofname)
