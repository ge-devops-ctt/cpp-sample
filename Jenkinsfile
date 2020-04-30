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
* Clear old tests
*/
 def clearOldTests(xrayFeatureFilesPath) {
    sh "rm -rf ${xrayFeatureFilesPath}"
 }

 /*
 * Export ":" delimited test definition  
 */ 
 def exportGenericTests(project, testPlan) {
    withCredentials([usernamePassword(credentialsId: JIRA_CREDENTIALS_ID, passwordVariable: 'PASSWORD', usernameVariable: 'USER')]) {
        tests = sh( 
            script: "python parser.py export --type=generic --project=${project} --test-plan=${testPlan}",
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
     sh "cd build/bin && ./GoogleTests --gtest_output=xml --gtest_filter=${test}"
}

/** 
* Import Test Execution results in Xray
*/
def importTestExecutionResults(project, testPlan, revision, resultsFilePath) {
    withCredentials([usernamePassword(credentialsId: JIRA_CREDENTIALS_ID, passwordVariable: 'PASSWORD', usernameVariable: 'USER')]) {
        sh "python parser.py import --project ${project} --test-plan=${testPlan} --revision ${revision} --report-file ${resultsFilePath} --type junit"
    }
}



