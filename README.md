# AWS Lambda Audit
Because an attacker gaining access to your AWS account can do 
[malicious things in Lambda](http://hypn.za.net/blog/2017/08/23/aws-lambda-mischief/), this Python script will check all 
versions of your AWS Lambda functions for unusual file sizes.

It makes use of the popular "Boto3" library and expects your local environment to be [setup with AWS credentials and region](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

## Usage:

	python lambda-audit.py -h
	usage: lambda-audit.py [-h] [-c COMPARISON] [-d DEVIATION] [-v]

	optional arguments:
	  -h, --help            show this help message and exit
	  -c COMPARISON, --comparison COMPARISON
	                        "average" size, or "latest" version's size, to use for
	                        comparison
	  -d DEVIATION, --deviation DEVIATION
	                        deviation percent allowed
	  -v, --verbose         display some progress info

## Example:

	python lambda-audit.py -c latest -d 25 -v
	Checking 41 lambda functions...
	Checking 4 version(s) of function "list-books"
 	* "list-books" version 2 is larger than latest size (37.7MB > 17.77MB, with 25.0% deviation allowed)
	Checking 8 version(s) of function "update-book"
 	* "update-book" version 1 is smaller than latest size (17.69MB < 31.15MB, with 25.0% deviation allowed)
 	* "update-book" version 2 is smaller than latest size (17.75MB < 31.15MB, with 25.0% deviation allowed)
 	* "update-book" version 3 is smaller than latest size (17.79MB < 31.15MB, with 25.0% deviation allowed)
 	* "update-book" version 4 is smaller than latest size (17.79MB < 31.15MB, with 25.0% deviation allowed)
 	* "update-book" version 5 is smaller than latest size (17.88MB < 31.15MB, with 25.0% deviation allowed)
	Checking 2 version(s) of function "delete-book"
	...