from elasticsearch import Elasticsearch
import json

def query_by_ident(index='_all' ,host=None, port=9200, ident=None, size=500, ip=0):
    """
    Return array log
    :host: ip elasticsearch
    :port: port of elasticsearch server (default 9200)
    :ident: tu khoa dung de match du lieu
    :size: so luong data lay ra (default 500)
    :index: index of elasticsearch
    :ip: ip address thomson
    """
    query = {
        "sort": [{"@timestamp": "desc"}],
        "from": 0,
        "size": 2,
        "_source": ["message"],
        "query": {
          "bool": {
            "must": [
              {
                "match": {
                  "ident.keyword": "Monitor"
                }
              },
              {
                "match": {
                  "message": "origin"
                }
              },
              {
                "match": {
                  "message": "hni"
                }
              },
              {
                "match": {
                  "message": "down"
                }
              },
              {
                "match": {
                  "message": "239.1.2.17"
                }
              }
            ],
            "filter": {
              "range": {
                "@timestamp": {
                  "gte": "now-24h",
                  "lte": "now"
                }
              }
            }
          }
        },
        "sort": [
          {
            "@timestamp": {
              "order": "DESC"
            }
          }
        ]
      }
    elast = Elasticsearch([{'host':host, 'port': port}]).search(index= index,body = query,)
    #print query
    print len(elast['hits']['hits'])
    return elast['hits']['hits']

aa = query_by_ident(index='_all' ,host="183.80.133.166", port=9200, ident=None, size=500, ip="172.29.70.189")
for i in aa:
    tmp = i["_source"]["message"]
    log = json.loads(tmp[tmp.find("{"):tmp.find("}")+1])
    print log["desc"]