import os
import sys
import glob
from elasticsearch import Elasticsearch
es = Elasticsearch("192.168.0.201")
import base64

# clear index
s = es.search(index='check_finereader', doc_type='my_type', q='', _source_exclude=['data'])
for doc in s['hits']['hits']:
    es.delete(id=doc['_id'], doc_type='my_type', index='check_finereader')

# add docs to index
results = []
for f in glob.glob(os.path.join(sys.argv[1], '*.*')):
    with open(f, 'rb') as fh:
        data = base64.b64encode(fh.read()).decode('ascii')
        doc = {'filename' : os.path.basename(f),
               'data': data}
        result = es.index(index='check_finereader',
                          doc_type='my_type',
                          pipeline='attachment',
                          body=doc)
        results.append(result)

# compare contents extracted
docids = [r['_id'] for r in results]
docs = [es.get(index='check_finereader', doc_type='my_type', id=id, _source_exclude=['data'])
        for id in docids]
