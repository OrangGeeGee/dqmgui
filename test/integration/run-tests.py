import time
import unittest
import re
import requests


class SessionTest(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://dqmgui-integration-1:8060/dqm/dev/'
        print 'setUp'

    def tearDown(self):
        print 'tearDown'

    def test_session(self):
        print 'Running tests'
        # time.sleep(5)
        # todo upload root file with visDQMUpload
        print 'Should have uploaded the .root file by now'
        print 'Starting verification...'

        print 'Calling url ' + self.base_url
        create_session_response = requests.get(self.base_url)
        self.assertTrue(create_session_response.ok,
                        'Request failed. Status code received ' + str(create_session_response.status_code))

        session = re.search('/dqm/dev/session/([\w\d]+)', str(create_session_response.content))

        choose_sample_url = self.base_url + 'session/' + session.group(1) + '/chooseSample?vary=run;order=dataset'
        print 'Calling url ' + str(choose_sample_url)
        choose_sample_response = requests.get(choose_sample_url)
        self.assertTrue(choose_sample_response.ok,
                        'Request failed. Status code received ' + str(choose_sample_response.status_code))

        print str(choose_sample_response.content)

        # todo find out why response has (<json>) format???
        # json = choose_sample_response.json()
        # print str(json)


if __name__ == '__main__':
    unittest.main()
