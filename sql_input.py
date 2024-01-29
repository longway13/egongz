import sys
import logging
import rds_config
import pymysql
import json
from tqdm import tqdm
# rds settings
rds_host = "ysu-team-003-rds.cnmgd1eiu1rn.ap-northeast-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_path = "everytime_computer_data.json"
data = []

with open("everytime_computer_data.json", 'r', encoding='UTF-8') as f:
    for line in f:
        data.append(json.loads(line))

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
item_count = 0

with conn.cursor() as cur:
    cur.execute('''
            DELETE FROM ComputerScience
        ''')
        
    cur.execute('''
            DELETE FROM ComputerScience_comment
        ''')
        
    cur.execute('''
            CREATE TABLE IF NOT EXISTS ComputerScience (
                title VARCHAR(255),
                detail VARCHAR(255),
                likes VARCHAR(10) NOT NULL,
                comments_count VARCHAR(10) NOT NULL,
                scraps VARCHAR(10) NOT NULL,
                url VARCHAR(40) PRIMARY KEY,
                timestamp VARCHAR(20) NOT NULL
            )
        ''')

    cur.execute('''
            CREATE TABLE IF NOT EXISTS ComputerScience_comment (
                url VARCHAR(40) NOT NULL,
                Type VARCHAR(10) NOT NULL,
                Author VARCHAR(10) NOT NULL,
                Comment VARCHAR(255) NOT NULL,
                Timestamp VARCHAR(20) NOT NULL,
                Vote_Count VARCHAR(5) NOT NULL
            )
        ''')

    # 데이터 삽입
    for i in tqdm(range(len(data)),"mysql process"):
        # URL이 이미 존재하는지 확인
        cur.execute("SELECT COUNT(*) FROM ComputerScience WHERE url = %s", (data[i]["url"],))
        result = cur.fetchone()[0]

        # URL이 존재하지 않으면 데이터 삽입
        if result == 0:
            item_count += 1
            # ComputerScience 테이블에 삽입
            cur.execute('''
                INSERT INTO ComputerScience (title, detail, likes, comments_count, scraps, url, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (data[i]["title"], data[i]["detail"], data[i]["likes"], data[i]["comments_count"], data[i]["scraps"], data[i]["url"], data[i]["timestamp"]))
            # ComputerScience_comment 테이블에 댓글 삽입
            for comment in data[i]["comments"]:
                cur.execute('''
                    INSERT INTO ComputerScience_comment (url, Type, Author, Comment, Timestamp, Vote_Count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (data[i]["url"], comment["Type"], comment["Author"], comment["Comment"], comment["Timestamp"], comment["Vote Count"]))

    # 변경사항 저장
    conn.commit()
print("Added %d items from RDS MySQL table" % (item_count))
