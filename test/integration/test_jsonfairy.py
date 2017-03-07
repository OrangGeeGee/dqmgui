import requests

import base
import rootgen


class JsonFairyTest(base.BaseIntegrationTest):
    def test_pixel_histograms(self):
        (filename, run, dataset) = self.prepareIndex({
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

        print 'Starting verification...'
        histogram_url = '%sjsonfairy/archive/%d%s/Pixel/AdditionalPixelErrors/FedChNErr?formatted=false'\
                        % (self.base_url, run, dataset)
        histogram_response = requests.get(histogram_url)
        print 'Histogram fetched from %s with status %d' % (histogram_url, histogram_response.status_code)
        self.assertTrue(histogram_response.ok,
                        'Request failed. Status code received ' + str(histogram_response.status_code))
        histogram_json = histogram_response.json()
        print str(histogram_json)