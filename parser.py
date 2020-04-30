import requests
from requests.auth import HTTPBasicAuth
from os import environ
import argparse
import sys
import re
import subprocess


def get(endpoint, parameters):

    url = f"{jira_url}{endpoint}?{parameters}"

    try:
        r = requests.get(url, auth=HTTPBasicAuth(user, password))
        r.raise_for_status()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)

    tests = r.json()
    tests_defintion = [d['definition'] for d in tests]
    if tests_defintion:
        return ':'.join(tests_defintion)
    else:
        sys.exit("No tests found")

def post(endpoint, parameters, files):
    url = f"{jira_url}{endpoint}?{parameters}"

    try:
        r = requests.post(url, auth=HTTPBasicAuth(user, password), files=files)
        print(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    print(r.json())

def post_junit(project, test_plan, revision, junit_report):
    revision_list = revision.split('.')
    fix_version = f"v{revision_list[0]}.{revision_list[1]}"
    print(fix_version)
    endpoint = "/rest/raven/1.0/import/execution/junit"
    parameters = f"projectKey={project}&testPlanKey={test_plan}&revision={revision}&fixVersion={fix_version}"
    files = {'file': open(junit_report, 'rb')}
    post(endpoint, parameters, files)

def fix_version(revision):
    return 

def get_tests(project, test_plan):
    endpoint = "/rest/raven/1.0/api/test"
    parameters = f"jql=project = {project} AND cf[37500] = Generic AND issue in testplantests('{test_plan}')".replace(" ", "%20")
    return get(endpoint, parameters)

def import_test_execution(args):
    if args.type == "junit":
        post_junit(args.project, args.test_plan, args.revision, args.report_file)

def export_test_execution(args):
    if args.type == "generic":
        print(get_tests(args.project, args.test_plan))   

def revision_regex(arg_value, pat=re.compile(r"^[0-9]\.[0-9]\.[0-9].*")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

def parsing():

    parser = argparse.ArgumentParser(description="The parent parser")

    subparsers = parser.add_subparsers(title="actions")

    parent_parser = argparse.ArgumentParser(add_help=True)
    parent_parser.add_argument("--project", required=True, help="Jira project")
    parent_parser.add_argument("--test-plan", required=True, help="Test plan to select")

    parser_export = subparsers.add_parser("export", parents=[parent_parser],
                                        add_help=False,
                                        description="The export parser",
                                        help="Export tests")
    parser_export.add_argument("--type", required=True, help="type of tests", choices=["generic", "cucumber"])

    parser_export.set_defaults(func=export_test_execution)

    parser_import = subparsers.add_parser("import", parents=[parent_parser],
                                        add_help=False,
                                        description="The import parser",
                                        help="Import tests results")
    parser_import.add_argument("--revision", required=True, type=revision_regex, help="Revision of the test execution")
    parser_import.add_argument("--report-file", required=True, help="Report file of the test execution")
    parser_import.add_argument("--type", required=True, help="Type of report", choices=["cucumber", "junit"])
    parser_import.set_defaults(func=import_test_execution)

    args = parser.parse_args()
    args.func(args)
    
def init():
    MANDATORY_ENV_VARS = ["USER", "PASSWORD", "JIRA_URL"]

    for var in MANDATORY_ENV_VARS:
        if var not in environ:
            raise EnvironmentError("Failed because {} is not set.".format(var))
    global user, password, jira_url
    user = environ["USER"]
    password = environ["PASSWORD"]
    jira_url = environ["JIRA_URL"]

def main():
    init()
    parsing()    
    
main()
