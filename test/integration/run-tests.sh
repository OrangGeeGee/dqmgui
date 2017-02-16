#!/usr/bin/env sh
# should be run from /data/srv on Docker image
# todo rework this script to python test class
. current/apps/dqmgui/128/etc/profile.d/env.sh
for s in current/*/*/*/*/*/etc/profile.d/init.sh; do . $s; done
cd BUILD
monDistPatch -s DQM
cd ..
visDQMUpload http://dqmgui-integration-1:8060/dqm/dev/ BUILD/test/integration/DQM_V0001_R000000001__RelValGluGluToHHTo4B_node_SM_14TeV-madgraph__CMSSW_8_2_0_PhaseIIFall16LHEGS82-90X_upgrade2023_realistic_v1-genvalid-v0__DQM.root
