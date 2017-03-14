import unittest
import ConfigParser
import hashlib
import json
import os
import subprocess
import re
import time
import shutil
import tempfile
import urllib2
from stat import ST_SIZE
from sys import stdout

import rootgen


class UploadWatchTimeout(Exception):
    pass


class BaseIntegrationTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config.read(script_dir + '/config.cfg')
        self.base_url = config.get('dqm', 'base_url')
        self.upload_watch_interval = float(config.get('dqm', 'upload_watch_interval'))
        self.upload_watch_retries = int(config.get('dqm', 'upload_watch_retries'))
        self.temp_dir = tempfile.mkdtemp()
        print 'setUp'

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        print 'tearDown'

    def upload(self, filename, path):

        try:
            subprocess.check_call(["visDQMUpload", self.base_url, path])
        except (OSError, subprocess.CalledProcessError) as e:
            print 'visDQMUpload script invokation failed'
            print e
            try:
                self.upload_requests(filename, path)
            except ImportError as e:
                print 'Either visDQMUpload must be available on path or requests library must be installed manually.'
                raise e

    def upload_requests(self, filename, path):
        import requests

        url = self.base_url + 'data/put'
        files = {'file': (filename, open(path, 'rb'))}
        data = {'size': str(os.stat(path)[ST_SIZE]),
                'checksum': 'md5:%s' % hashlib.md5(file(path).read()).hexdigest()}
        headers = {'User-agent': 'Integration tests'}
        response = requests.post(url, data=data, files=files, headers=headers)

        print 'Uploaded. HTTP Status: %d, DQM-Status-Code: %s, DQM-Status-Message: %s, DQM-Status-Detail: %s, Body: %s' \
              % (response.status_code, response.headers['DQM-Status-Code'], response.headers['DQM-Status-Message'],
                 response.headers['DQM-Status-Detail'], response.content)

    def prepareIndex(self, content):
        (filename, run, dataset, path) = rootgen.create_file(content, directory=self.temp_dir)
        self.upload(filename, path)
        self.uploadWatch(dataset)

        return filename, run, dataset

    def session(self):
        create_session_response = urllib2.urlopen(self.base_url)
        create_session_content = create_session_response.read()
        self.assertEquals(create_session_response.getcode(), 200, 'Request failed. Status code received not 200')

        session = re.search('/dqm/dev/session/([\w\d]+)', create_session_content)
        return session.group(1)

    def chooseSample(self, session):
        choose_sample_url = '%ssession/%s/chooseSample?vary=run;order=dataset' % (self.base_url, session)
        response = urllib2.urlopen(choose_sample_url)
        content = response.read()
        self.assertEquals(response.getcode(), 200, 'Request failed. Status code re1ceived not 200')
        content = re.sub('\)$', '', re.sub('^\(', '', content)).replace('\'', '"')
        json_content = json.loads(content)
        return json_content

    def uploadWatch(self, dataset):
        stdout.write('Upload watch started for dataset %s. Checking every %s seconds' % (dataset, self.upload_watch_interval))
        stdout.flush()
        session = self.session()
        start_time = time.time()
        i = 0
        while i < self.upload_watch_retries:
            time.sleep(self.upload_watch_interval)
            stdout.write('.')
            stdout.flush()
            choose_sample_json = self.chooseSample(session)
            for types in choose_sample_json[1]['items']:
                for item in types['items']:
                    if dataset == item['dataset']:
                        print ''
                        print 'Dataset %s found in %.3f with type %s, run %s, importversion %s, version %s' \
                              % (dataset, (time.time() - start_time), item['type'], item['run'], item['importversion'],
                                 item['version'])
                        return True
            i += 1

        raise UploadWatchTimeout()
