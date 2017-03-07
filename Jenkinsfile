node('dqmgui-ci-worker') {
    stage('Build') {
        checkout scm
        sh "env"
        sh "id"
        sh "pwd"
        sh "ls -al"
        sh "ls -al /data/srv"
        sh "monDistPatch -s DQM"
    }
    stage('Start') {
        sh '/data/srv/current/config/dqmgui/manage -f dev start "I did read documentation"'
    }
    stage('Test') {
        sh "python --version"
        sh "python -m unittest test/integration"
    }
    stage('Index regression') {
        // TODO extract and validate new code works with old index
        sh "wget https://rovere.web.cern.ch/rovere/test_index.tar.bz2"
        // sh "for sample in {1..7}; do echo -n "$sample " && visDQMIndex dump --sample $sample test_index/ data 2>&1 >/dev/null | wc -l ; done"
    }
}