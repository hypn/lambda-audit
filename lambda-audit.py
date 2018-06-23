import boto3
import argparse

def pretty_size(bytes):
	return str(round(float(bytes) / 1024 / 1024, 2)) + 'MB'

def get_lambda_functions(client):
	response = client.list_functions()
	return map(lambda x: x.get('FunctionName', False), response['Functions'])

def get_function_versions(client, name):
	response = client.list_versions_by_function(FunctionName=name)
	return map(lambda x: x.get('Version', False), response['Versions'])

def get_function_version_info(client, name, version):
	response = client.get_function(FunctionName=name, Qualifier=version)
	return {
		'version': version,
		'codeSize': response['Configuration']['CodeSize'],
		'codeLocation': response['Code']['Location']
	}

def run():
	client = boto3.client('lambda')

	functions = get_lambda_functions(client)
	if verbose:
		print 'Checking ' + str(len(functions)) + ' lambda functions...'

	for function in functions:
		versions = get_function_versions(client, function)
		version_info = map(lambda i: get_function_version_info(client, function, i), versions)

		num_versions = len(versions)
		if verbose:
			print 'Checking ' + str(num_versions) + ' version(s) of function "' + function + '"'

		if comparisonSize == 'latest':
			size_limit = version_info[-1]['codeSize']
		else:
			total_size = 0
			for info in version_info:
				total_size += info['codeSize']
			size_limit = total_size / num_versions

		lower_size = (size_limit * (1.00 - (deviation / 100)))
		upper_size = (size_limit * (1.00 + (deviation / 100)))

		for info in version_info:
			if (info['codeSize'] < size_limit) and (info['codeSize'] < lower_size):
				print ' * "' + function + '" version ' + str(info['version']) + ' is smaller than ' + comparisonSize + ' size (' + pretty_size(info['codeSize']) + ' < ' + pretty_size(size_limit) + ', with ' + str(deviation) + '% deviation allowed)'

			if (info['codeSize'] > size_limit) and (info['codeSize'] > upper_size):
				print ' * "' + function + '" version ' + str(info['version']) + ' is larger than ' + comparisonSize + ' size (' + pretty_size(info['codeSize']) + ' > ' + pretty_size(size_limit) + ', with ' + str(deviation) + '% deviation allowed)'

# setup command line arguments
ap = argparse.ArgumentParser()
ap.add_argument('-c', '--comparison', help='"average" size, or "latest" version\'s size, to use for comparison')
ap.add_argument('-d', '--deviation', type=float, help='deviation percent allowed')
ap.add_argument('-v', '--verbose', action='store_const', const=True, help='display some progress info')
args = vars(ap.parse_args())

# default settings:
verbose = False
deviation = 15.00
comparisonSize = 'average'

# set settings from arguments
if args.get('comparison') == 'latest':
	comparisonSize = 'latest'
if args.get('deviation'):
	deviation = args.get('deviation')
if args.get('verbose') == True:
	verbose = True

run()