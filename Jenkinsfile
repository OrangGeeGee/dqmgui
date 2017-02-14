pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                ls -al
                ls -al /data/srv
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
    }
}