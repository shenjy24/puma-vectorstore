## 一. 环境搭建
> 操作系统：Mac 
> 
> 虚拟环境：venv
> 
> Milvus: 2.4.0

### 1. 本地部署 Milvus
#### (1) Linux 或者 Mac环境
```
wget https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
bash standalone_embed.sh start
```

#### (2) Windows 环境：使用 docker-compose 部署

```dockerfile
version: '3.5'

services:
  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.0
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/etcd:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2020-12-03T00-03-10Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/minio:/minio_data
    command: minio server /minio_data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:2.4-latest
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
    ports:
      - "19530:19530"
    depends_on:
      - "etcd"
      - "minio"

networks:
  default:
    name: milvus
```

执行指令：
```
docker-compose up -d
```

### 2. 部署 Attu (Milvus GUI)
```
docker run -d --name milvus-gui  -p 8000:3000 -e MILVUS_URL=172.17.0.1:19530 zilliz/attu
```
- MILVUS_URL 不能设置为 localhost 或 127.0.0.1，因为 Milvus 是部署在 Docker 中，需要使用 172.17.0.1
- 如果使用 docker-compose 启动的，记得添加 `--network=milvus`