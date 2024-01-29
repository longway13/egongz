import json
from elasticsearch import Elasticsearch
from requests_aws4auth import AWS4Auth
from tqdm import tqdm
import elastic_config

# Elasticsearch 엔드포인트 설정
es_endpoint = elastic_config.es_endpoint
es_username = elastic_config.es_username
es_password = elastic_config.es_password

# Elasticsearch에 연결
es = Elasticsearch([es_endpoint], basic_auth=(es_username, es_password))

# elastictest 인덱스의 모든 데이터 삭제
es.indices.delete(index='elastictest', ignore=[400, 404])

rows = []

with open("everytime_computer_data.json", 'r', encoding='UTF-8') as f:
    for line in f:
        rows.append(json.loads(line))

for index in tqdm(range(len(rows)), desc="Adding documents to Elasticsearch"):
    json_object = {
        "title": rows[index]["title"],
        "detail": rows[index]["detail"],
        "likes": rows[index]["likes"],
        "comments_count": rows[index]["comments_count"],
        "scraps": rows[index]["scraps"],
        "url": rows[index]["url"],
        "comments": rows[index]["comments"],
        "timestamp": rows[index]["timestamp"]
    }

    es.index(index='elastictest', body=json.dumps(json_object))

print("Success: All documents added to elastictest index.")
