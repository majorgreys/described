import os
import sys
import base64
import click
from glob import glob
import json

from elasticsearch import Elasticsearch

@click.group()
def cli():
    pass

def initializeEs(host):
    es = Elasticsearch(host)
    # Create pipeline to use Ingest Attachment Processor Plugin
    body = {
        "description": "Extract attachment information",
        "processors": [
            {
                "attachment": {
                    "field": "data"
                }
            }
        ]
    }
    es.index(index='_ingest', doc_type='pipeline', id='attachment', body=body)
    return es

def indexfile(es, path):
    with open(path, 'rb') as fh:
        data = base64.b64encode(fh.read()).decode('ascii')
        doc = {
            'filename' : os.path.basename(path),
            'data': data
        }
        result = es.index(
            index='pdig',
            doc_type='mytype',
            pipeline='attachment',
            body=doc
        )
        if result:
            return result['_id']

@cli.command()
@click.argument('host')
@click.argument('query')
def search(host, query):
    es = Elasticsearch(host)
    result = es.search(
        index='pdig',
        doc_type='mytype',
        q=query,
        _source_exclude=['data']
    )
    print([
        '{}: {}'.format(
            hit['_source']['filename'],
            hit['_source']['attachment']['content'][:25]
        )
        for hit in result['hits']['hits']
    ])

@cli.command()
@click.argument('host')
@click.argument('output')
def dump(host, output):
    es = Elasticsearch(host)
    result = es.search(
        index='pdig',
        body={"query": {"match_all": {}}},
        _source_exclude=['data']
    )
    with open(output, 'w') as f:
        json.dump(result['hits']['hits'], f)

@cli.command()
@click.argument('host')
@click.argument('path', type=click.Path(exists=True))
def index(host, path):
    paths = glob(os.path.join(path, '*.pdf'))
    click.echo(
        'Running ElasticSearch indexing over {} files in {}...'.format(
            len(filepaths),
            path
        )
    )
    es = initializeEs(host)
    docids = []
    with click.progressbar(paths) as bar:
        for fp in bar:
            docid = indexfile(es, fp)
            if docid:
                docids.extend(docid)
    click.echo('{} documents indexed'.format(len(docids)))

if __name__ == '__main__':
    cli()
