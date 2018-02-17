import docopt, yaml, sys

usage = \
'''
Usage: 
        contributors.py print FILE [--quiet]

Options:
        --quiet                do not print to stdout 

'''

if( __name__ == "__main__"):
	args = docopt.docopt(usage)

	try:
		f = open(args["FILE"])
	except Exception as e:
		print(e, file = sys.stdout)
		sys.exit(1)

	try:
		data = yaml.load(f)
	except Exception as e:
		print(e, file = sys.stdout)
		sys.exit(1)

	for contributor in data:
		try:
			string = "{name} (mailto:{email})".format(**contributor)
			contributions = "".join(["\t[{year}] {descr}\n".format(**c) for c in contributor["contributions"]])
		except Exception as e:
			print(e, file = sys.stdout)
			print("Dataset was:", file = sys.stdout)
			print(contributor, file = sys.stdout)
			sys.exit(1)
		if(not args["--quiet"]):
			print(string)
			print(contributions)

	sys.exit(0)
		

