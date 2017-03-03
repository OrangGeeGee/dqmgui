import hashlib
import os
import re
import unittest
from stat import ST_SIZE

import requests
import time

import rootgen


class SessionTest(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://dqmgui-integration-1:8060/dqm/dev/'
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

    def test_session(self):
        print 'Running tests'

        (filename, run, dataset) = rootgen.create_file({
            '/DQMData/Run 1/Pixel/Run summary/AdditionalPixelErrors': [
                 {'name': 'FedChNErr', 'gen': rootgen.TH1F},
                 {'name': 'FedChLErr', 'gen': rootgen.TH1F, 'type': 'TH2F'},
                 {'name': 'FedETypeNErr', 'gen': rootgen.TH1F, 'type': 'TH2F'},
             ],
            '/DQMData/Run 283560/Pixel/Run summary/AdditionalPixelErrors/FED_0': [
                 {'name': 'FedETypeNErr_siPixelDigis_0', 'gen': rootgen.TH1F},
             ],
            '/DQMData/Run 1/Pixel/Run summary': [
                 {'name': 'averageDigiOccupancy', 'gen': rootgen.TH1F, 'type': 'TProfile'}],
            '/DQMData/Run 1/Pixel/Run summary/Barrel': [
                 {'name': 'SUMOFF_charge_OnTrack_Barrel', 'gen': rootgen.TH1F},
                 {'name': 'SUMOFF_nclusters_OnTrack_Barrel', 'gen': rootgen.TH1F},
                 {'name': 'SUMOFF_size_OnTrack_Barrel', 'gen': rootgen.TH1F}],
            '/DQMData/Run 1/Pixel/Run summary/Endcap': [
                 {'name': 'SUMOFF_charge_OnTrack_Endcap', 'gen': rootgen.TH1F},
                 {'name': 'SUMOFF_nclusters_OnTrack_Endcap', 'gen': rootgen.TH1F},
                 {'name': 'SUMOFF_size_OnTrack_Endcap', 'gen': rootgen.TH1F}]

        })

        self.upload(filename)

        # todo ping server to know if file successfully uploaded
        time.sleep(30)
        print '30 seconds passsed. Should have uploaded the .root file by now'

        print 'Calling url ' + self.base_url
        create_session_response = requests.get(self.base_url)
        self.assertTrue(create_session_response.ok,
                        'Request failed. Status code received ' + str(create_session_response.status_code))

        session = re.search('/dqm/dev/session/([\w\d]+)', str(create_session_response.content))

        choose_sample_url = '%ssession/%s/chooseSample?vary=run;order=dataset' % (self.base_url, session.group(1))
        print 'Calling url ' + str(choose_sample_url)
        choose_sample_response = requests.get(choose_sample_url)
        self.assertTrue(choose_sample_response.ok,
                        'Request failed. Status code received ' + str(choose_sample_response.status_code))
        print str(choose_sample_response.content)

        print 'Starting verification...'
        histogram_url = '%sjsonfairy/archive/%d%s/Pixel/AdditionalPixelErrors/FedChNErr?formatted=false' % (self.base_url, run, dataset)
        histogram_response = requests.get(histogram_url)
        print 'Histogram fetched from %s with status %d' % (histogram_url, histogram_response.status_code)
        self.assertTrue(histogram_response.ok,
                        'Request failed. Status code received ' + str(histogram_response.status_code))
        histogram_json =histogram_response.json()
        print str(histogram_json)


if __name__ == '__main__':
    unittest.main()
