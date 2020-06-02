import groovy.json.JsonSlurper

pipeline {
    agent none 
    environment {
        JIRA_CREDENTIALS_ID="9966b33c-2ec1-4f41-9419-b4ed1128a8cd"
        TEST_PLAN="SWFTY-395"
        JIRA_URL="https://stamp.gs.ec.ge.com/jira"
        JIRA_PROJECT="SWFTY"
        RESULTS_FILE_PATH = "build/bin/test_detail.xml"
        TEST_EXECUTION_VERSION = '1.1.0-alpha.1'

    }
    options {
        skipDefaultCheckout()
        buildDiscarder(logRotator(artifactDaysToKeepStr: '1', artifactNumToKeepStr: '1', daysToKeepStr: '5', numToKeepStr: '10'))
        disableConcurrentBuilds()
	}
    stages {
        stage('Test Xray API') {
            agent {
                docker { 
                    image 'conanio/gcc8'
                }
            }
            steps {
                script {
                    checkout scm
                    installXrayConnector()
                    
                    tests = exportGenericTests(JIRA_PROJECT, TEST_PLAN)
                    runTests(tests)                    
                }
            }
            post {
                always {
                   importTestExecutionResults(JIRA_PROJECT, TEST_PLAN, TEST_EXECUTION_VERSION, RESULTS_FILE_PATH)     
                }
            }
        }
    }
}

/*
* Install Xray connector
*/
 def installXrayConnector() {
    dir('xray-connector') {
        git credentialsId: 'CBT_GITHUB_TOKEN', 
            branch: 'develop', 
            url: 'https://github.build.ge.com/devops-ctt-demo/xray-connector'
        
        sh "ls -l"
        sh "pip install -r requirements.txt && pip install -e ."
    }
 }

 /*
 * Export ":" delimited test definition  
 */ 
 def exportGenericTests(project, testPlan) {
    withCredentials([usernamePassword(credentialsId: JIRA_CREDENTIALS_ID, passwordVariable: 'PASSWORD', usernameVariable: 'USER')]) {
        tests = sh( 
            script: "xray-connector export --type=generic --project=${project} --test-plan=${testPlan} --test-runner=googletest",
            returnStdout: true
        )
        return tests
    }
 }

 /*
 * Run tests
 */
def runTests(tests) {
     sh "./conan-configure.sh"
     sh "./build.sh"
     sh "cd build/bin && ./GoogleTests --gtest_output=xml --gtest_filter=${tests}"
}

/** 
* Import Test Execution results in Xray
*/
def importTestExecutionResults(project, testPlan, revision, resultsFilePath) {
    withCredentials([usernamePassword(credentialsId: JIRA_CREDENTIALS_ID, passwordVariable: 'PASSWORD', usernameVariable: 'USER')]) {
        sh "xray-connector import-test-results --project ${project} --test-plan=${testPlan} --revision ${revision} --report-file ${resultsFilePath} --type junit"
        
    }
}



