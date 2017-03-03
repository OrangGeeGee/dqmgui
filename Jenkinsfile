node('dqmgui-ci-worker') {
    stage('Build') {
        sh "id"
        sh "pwd"
        sh "ls -al"
        sh "ls -al /data/srv"
        checkout scm
        wget https://rovere.web.cern.ch/rovere/test_index.tar.bz2
    }
    stage('Test') {„
        echo 'Testing..'
    }
}