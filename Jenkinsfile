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
    stage('Start') {
        // start server in development mode, wait for it to start and print logs
        sh '''
            source /data/srv/current/apps/dqmgui/128/etc/profile.d/env.sh
            /data/srv/current/config/dqmgui/manage -f dev start "I did read documentation"
            ps aux | grep dqm
            sleep 10
            ps aux | grep dqm
            for i in /data/srv/logs/dqmgui/dev/*; do echo $i:; cat $i; done
        '''
    }
    stage('Integration Test') {
        // integration tests use visDQMUpload script or requests library, so we setup DQM env variables before running
        sh '''
            ps aux | grep dqm
            source /data/srv/current/apps/dqmgui/128/etc/profile.d/env.sh
            cd test/integration
            python -m unittest discover -v
        '''
    }
    stage('Index regression') {
        // TODO extract and validate new code works with old index
        sh "wget https://rovere.web.cern.ch/rovere/test_index.tar.bz2"
        // sh "for sample in {1..7}; do echo -n "$sample " && visDQMIndex dump --sample $sample test_index/ data 2>&1 >/dev/null | wc -l ; done"
    }
}