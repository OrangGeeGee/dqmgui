node('dqmgui-ci-worker') {
    stage('Build') {
        checkout scm
        // environment debug
        sh '''
            id
            pwd
            python --version
            env
            ls -al
            ls -al /data/srv
        '''

        // init environment variables and patch the version in the image with latest from repository
        sh '''
            for s in /data/srv/current/*/*/*/*/*/etc/profile.d/init.sh; do . $s; done
            source /data/srv/current/apps/dqmgui/128/etc/profile.d/env.sh
            monDistPatch -s DQM
        '''
    }
    stage('Integration Test') {
        // start server in development mode and run integration tests
        sh '''
            source /data/srv/current/apps/dqmgui/128/etc/profile.d/env.sh
            /data/srv/current/config/dqmgui/manage -f dev start "I did read documentation"
            cd test/integration
            python -m unittest discover
        '''
    }
    stage('Index regression') {
        // TODO extract and validate new code works with old index
        sh "wget https://rovere.web.cern.ch/rovere/test_index.tar.bz2"
        // sh "for sample in {1..7}; do echo -n "$sample " && visDQMIndex dump --sample $sample test_index/ data 2>&1 >/dev/null | wc -l ; done"
    }
}