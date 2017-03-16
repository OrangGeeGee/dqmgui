import json
import urllib2
import base
import rootgen


class JsonFairyTest(base.BaseIntegrationTest):
    def test_pixel_histograms(self):
        (filename, run, dataset) = self.prepareIndex({
            '/DQMData/Run 1/Pixel/Run summary/AdditionalPixelErrors': [
                {'name': 'FedChNErr', 'gen': rootgen.TH1F},
                {'name': 'FedChLErr', 'gen': rootgen.TH2F},
                {'name': 'FedETypeNErr.json', 'gen': rootgen.TH2F},
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
        histogram_response = urllib2.urlopen(histogram_url)
        histogram_content = histogram_response.read()
        print 'Histogram fetched from %s with status %d' % (histogram_url, histogram_response.getcode())
        self.assertEquals(histogram_response.getcode(), 200, 'Request failed. Status code re1ceived not 200')
        histogram_json = json.loads(histogram_content)
        print str(histogram_json)