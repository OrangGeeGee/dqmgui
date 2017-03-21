FROM gitlab-registry.cern.ch/asinica/dqmgui-ci-worker:slc6

ADD . /data/srv/BUILD/

RUN . current/apps/dqmgui/128/etc/profile.d/env.sh; \
    for s in current/*/*/*/*/*/etc/profile.d/init.sh; do . $s; done; \
    cd BUILD; \
    monDistPatch -s DQM; \
    cd ..

ENTRYPOINT /data/srv/current/config/dqmgui/manage -f dev start "I did read documentation" && bash