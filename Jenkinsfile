pipeline {
    agent {
        label: 'dqmgui-ci-worker'
    }

    stages {
        stage('Build') {
            steps {
                sh "ls -al"
                sh "ls -al /data/srv"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
    }
}