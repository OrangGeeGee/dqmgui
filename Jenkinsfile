node('dqmgui-ci-worker') {
    stage('Build') {
        checkout scm
        sh "for s in /data/srv/current/*/*/*/*/*/etc/profile.d/init.sh; do . $s; done"
        sh "monDistPatch -s DQM"
    }
    stage('Start') {
        sh "source /data/srv/current/apps/dqmgui/128/etc/profile.d/env.sh"
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