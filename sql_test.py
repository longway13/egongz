import sys
import logging
import rds_config
import pymysql
import json

# rds settings
rds_host = "ysu-team-003-rds.cnmgd1eiu1rn.ap-northeast-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_path = "everytime_computer_data.json"
test = []

with open(file_path, 'r', encoding='UTF-8') as json_file:
    data = json.load(json_file)

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
    for i in range(len(data["title"])):
        # URL이 이미 존재하는지 확인
        cur.execute("SELECT COUNT(*) FROM ComputerScience WHERE url = %s", (data["url"][i],))
        result = cur.fetchone()[0]

        # URL이 존재하지 않으면 데이터 삽입
        if result == 0:
            item_count += 1
            # ComputerScience 테이블에 삽입
            cur.execute('''
                INSERT INTO ComputerScience (title, detail, likes, comments_count, scraps, url, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (data["title"][i], data["detail"][i], data["likes"][i], data["comments_count"][i], data["scraps"][i], data["url"][i], data["timestamp"][i]))

            # ComputerScience_comment 테이블에 댓글 삽입
            for comment in data["comments"][i]:
                cur.execute('''
                    INSERT INTO ComputerScience_comment (url, Type, Author, Comment, Timestamp, Vote_Count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (data["url"][i], comment["Type"], comment["Author"], comment["Comment"], comment["Timestamp"], comment["Vote Count"]))

    # 변경사항 저장
    conn.commit()
print("Added %d items from RDS MySQL table" % (item_count))
