import datetime


def root_mkdir_p(folder):
    import ROOT as r

    r.gDirectory.cd('/')
    fullpath = ''
    for level in folder.split('/'):
        fullpath += '/%s' % level
        if not level == '':
            if not r.gDirectory.GetDirectory(level):
                r.gDirectory.mkdir(level)
            r.gDirectory.cd(fullpath)


def gen_filename():
    version = 'V0001'
    run = 1
    runstr = 'R00000' + str(run)
    dataset = 'IntegTest'
    era = 'era' + datetime.datetime.utcnow().isoformat().replace(':', '').replace('.', '')
    datatier = 'DQM'
    return (
        'DQM_%s_%s__%s__%s__%s.root' % (version, runstr, dataset, era, datatier),
        run,
        '/%s/%s/%s' % (dataset, era, datatier)
    )


def create_file(content):
    import ROOT as r
    (filename, run, dataset) = gen_filename()
    f = r.TFile(filename, 'RECREATE')
    generated = 0
    for (folder, histos) in content.items():
        root_mkdir_p(folder)
        for h in histos:
            # make param dependant histoh['type']
            generated += 1
            h['gen'](h['name'])
    f.Write()
    f.Close()
    print 'Created %s with %d histograms in %d folders' % (filename, generated, len(content))
    return filename, run, dataset


def TH1F(name):
    import ROOT as r
    bins = 200
    xmin = 0
    xmax = 10
    histo = r.TH1F(name, name, bins, xmin, xmax)
    histo.SetFillColor(45)
    for i in range(1, 10):
        histo.Fill(i)
    histo.Write()


def read_contents(filename):
    import ROOT as r

    f = r.TFile.Open(filename, 'read')
    scan_directory('')


def scan_directory(path):
    import ROOT as r
    directory = r.gDirectory.GetDirectory(path)
    keys = directory.GetListOfKeys()
    if len(keys) > 0:
        for key in keys:
            if key.IsFolder():
                step_into = '%s/%s' % (path, key.GetName())
                scan_directory(step_into)
            else:
                print '%s/%s %s' % (path, key.GetName(), key.GetClassName())
    else:
        print '%s empty' % path


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Root file manipulation utils")
    parser.add_argument('filename', metavar='FILENAME', type=str,
                        help='Filename to read')
    args = parser.parse_args()
    read_contents(args.filename)

