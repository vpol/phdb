import logging
import urllib
import tempfile
import hashlib
import transaction
from phdb.models import Record, records_id_seq, meta
from phdb.models.common import Session

__author__ = 'vpol'

log = logging.getLogger(__name__)

def file_loader(config):
    # try:
        c = config.get_settings()
        links = c.links
        reindex = []
        for l in links.split(','):
            url = l.strip()
            file_name = url.split('/')[-1]
            checksum = ''
            new_checksum = ''
            ## save file to a temporary place to check if we need to overwrite and reindex
            try:
                with open(c.data_path + '/' + file_name) as old_file:
                    checksum = hashlib.sha1(old_file.read()).hexdigest()
            except IOError, e:
                log.error('No file found, need to download')
                checksum = ''
            try:
                urllib.urlretrieve(url, c.data_path + '/' + file_name)
            except Exception, e:
                pass
            with open(c.data_path + '/' + file_name) as new_file:
                new_checksum = hashlib.sha1(new_file.read()).hexdigest()
            if not checksum == new_checksum:
                ## need to reindex
                reindex.append(c.data_path + '/' + file_name)
        return reindex

def reindex(config, files):
    session = Session()
    to_add = []
    for f in files:
        with open(f) as data_file:
            for line in data_file:
                try:
                    d_line = line.decode('cp1251')
                except Exception, e:
                    print line
                    continue
                else:
                    r = Record()
                    # r.id = meta.engine.execute(records_id_seq)
                    r.code, r.nfrom, r.nto, r.amount, r.operator, r.region = d_line.split(';')
                    if len(to_add) > 1000:
                        # print len(to_add)
                        session.add_all(to_add)
                        transaction.commit()
                        to_add = []
                    to_add.append(r)
            # print len(to_add)
            session.add_all(to_add)
            transaction.commit()
            to_add = []