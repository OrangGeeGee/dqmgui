node('dqmgui-ci-worker') {
    stage('Build') {
        sh "id"
        sh "pwd"
        sh "ls -al"
        sh "ls -al /data/srv"
        checkout scm
    }
    stage('Test') {
        echo 'Testing..'
    }
}