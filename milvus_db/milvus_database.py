from pymilvus import connections, db


def create_database(db_name):
    return db.create_database(db_name)


if __name__ == '__main__':
    # 需要先连接服务器
    conn = connections.connect(host="127.0.0.1", port=19530)
    # 创建数据库
    create_database("book")
