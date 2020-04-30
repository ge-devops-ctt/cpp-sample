# GoogleTest-sample

```bash
# Clone the git repository
git clone https://github.build.ge.com/devops-ctt-demo/GoogleTest-sample.git; cd googleTest-sample

# Run the docker container
docker run -it -w /code -v ${pwd}:/code conanio/gcc8 bash

# Set env variables
export JIRA_URL=https://stamp.gs.ec.ge.com/jira
export USER="<YOUR_SSO"
export PASSWORD="<YOUR_PASSWORD>"
export PROJECT=SWFTY
export TEST_PLAN=SWFTY-395
export REVISION=1.1.0-alpha.1
export RESULTS_FILE_PATH="build/bin/test_detail.xml"

# Get generic tests of a specific tests plan
tests=$(python parser.py export --type=generic --project=SWFTY --test-plan=SWFTY-395)

# Run the tests
./conan-configure
./build.sh
cd build/bin && ./GoogleTests --gtest_output=xml --gtest_filter=$tests

# Import results
cd ../..
python parser.py import --project $PROJECT --test-plan $TEST_PLAN --revision $REVISION --report-file $RESULTS_FILE_PATH --type junit




