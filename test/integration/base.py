import ConfigParser
import hashlib
import json
import os
import re
import unittest
from stat import ST_SIZE

import requests
import time

import rootgen


class UploadWatchTimeout(Exception):
    pass


class BaseIntegrationTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read('config.cfg')
        self.base_url = config.get('dqm', 'base_url')
        self.upload_watch_interval = float(config.get('dqm', 'upload_watch_interval'))
        self.upload_watch_retries = int(config.get('dqm', 'upload_watch_retries'))
        print 'setUp'

    def tearDown(self):
        print 'tearDown'

    def upload(self, filename):

        url = self.base_url + 'data/put'
        files = {'file': (filename, open(filename, 'rb'))}
        data = {'size': str(os.stat(filename)[ST_SIZE]),
                'checksum': 'md5:%s' % hashlib.md5(file(filename).read()).hexdigest()}
        headers = {'User-agent': 'Integration tests'}
        response = requests.post(url, data=data, files=files, headers=headers)

        print 'Uploaded. HTTP Status: %d, DQM-Status-Code: %s, DQM-Status-Message: %s, DQM-Status-Detail: %s, Body: %s' \
              % (response.status_code, response.headers['DQM-Status-Code'], response.headers['DQM-Status-Message'],
                 response.headers['DQM-Status-Detail'], response.content)

    def prepareIndex(self, content):
        (filename, run, dataset) = rootgen.create_file(content)
        self.upload(filename)
        self.uploadWatch(dataset)

        return filename, run, dataset

    def session(self):
        create_session_response = requests.get(self.base_url)
        self.assertTrue(create_session_response.ok,
                        'Request failed. Status code received ' + str(create_session_response.status_code))

        session = re.search('/dqm/dev/session/([\w\d]+)', str(create_session_response.content))
        return session.group(1)

    def chooseSample(self, session):
        choose_sample_url = '%ssession/%s/chooseSample?vary=run;order=dataset' % (self.base_url, session)
        response = requests.get(choose_sample_url)
        self.assertTrue(response.ok,
                        'Request failed. Status code received ' + str(response.status_code))
        content = response.content
        content = re.sub('\)$', '', re.sub('^\(', '', content)).replace('\'', '"')
        json_content = json.loads(content)
        return json_content

    def uploadWatch(self, dataset):
        print 'Upload watch started for dataset %s. Checking every %s seconds' % (dataset, self.upload_watch_interval),

        session = self.session()
        start_time = time.time()
        i = 0
        while i < self.upload_watch_retries:
            time.sleep(self.upload_watch_interval)
            print '.',
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
