import sys
import subprocess
import json
import yaml

from pathlib import Path
from random import randint

#import time

def execution(testfiles,pcap, logpath):

	subprocess.call(['suricata.sh', testfiles, pcap, logpath])

PCAP_SUFFIX = set([
	'.pcap'
	, '.pcapng'
	, '.cap'
])

def prepare_result_dir(res_dir, name)->Path:
	new_subdir = res_dir / Path(name)
	while new_subdir.exists():
		new_subdir = res_dir / Path('{}_{}'.format(name, str(randint(0, 999999))))
	new_subdir.mkdir()
	return new_subdir

def tortilla(script, test_files, res_dir):
	## prepare the tortilla
	def rescursive_execution(_dir):
		for p in _dir.iterdir():
			if p.is_dir():
				rescursive_execution(p)
			elif p.is_file() and p.suffix in PCAP_SUFFIX:
				new_subdir = prepare_result_dir(res_dir, p.stem)
				ret = subprocess.check_call([
					str(script)
					, str(test_files.absolute())
					, str( Path('/') / p.relative_to(test_files.parent) )
					, str(new_subdir.absolute())
					])
				log = new_subdir / Path('logs/eve.json')
				if not log.is_file():
					continue
				js = []
				with log.open() as _file:
					lines = _file.readlines()
					for line in lines:
						one = json.loads(line)
						if one['event_type'] == 'alert':
							js.append(one)
				alert_js = new_subdir / Path('extracted_alerts.yaml')
				with alert_js.open('w') as _file:
					yaml.dump(js, _file)
				

	## soak the tortilla in gasoline, burn at 65783 C° and serve
	return rescursive_execution



if __name__ == '__main__':
	test_files = Path(sys.argv[1])
	pcap_folder = test_files
	script = Path(sys.argv[2]).absolute()

	res_dir = Path('./results')
	if not res_dir.is_dir():
		res_dir.mkdir()
	
	lunch = tortilla(script.absolute(), test_files.absolute(), res_dir.absolute())
	lunch(test_files)

	# for f in pcap_folder.iterdir():
	# 	if f.is_dir():
	# 		new_subdir = res_dir / Path(f.name)
	# 		if not new_subdir.is_dir():
	# 			new_subdir.mkdir()
	# 		pies = [i for i in f.glob('*.pcap')]
	# 		pies += [i for i in f.glob('*.pcapng')]
	# 		if len(pies) == 0 :
	# 			continue
	# 		ret = subprocess.check_call([
	# 			str(script)
	# 			, str(test_files.absolute())
	# 			, str( Path('/testfiles')/ Path(new_subdir.name) / Path(pies[0].name))
	# 			, str(new_subdir.absolute())
	# 			])
	# 		log = new_subdir / Path('logs/eve.json')
	# 		if not log.is_file():
	# 			continue
	# 		js = []
	# 		with log.open() as _file:
	# 			lines = _file.readlines()
	# 			for line in lines:
	# 				one = json.loads(line)
	# 				if one['event_type'] == 'alert':
	# 					js.append(one)
	# 		alert_js = new_subdir / Path('extracted_alerts.yaml')
	# 		with alert_js.open('w') as _file:
	# 			yaml.dump(js, _file)
	# 		#time.sleep(100)
	# 		#ret.wait()
