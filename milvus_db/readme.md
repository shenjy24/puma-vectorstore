## 一. 环境搭建
> 操作系统：Mac 
> 
> 虚拟环境：venv
> 
> Milvus: 2.4.0

### 1. 本地部署 Milvus
```
wget https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
bash standalone_embed.sh start
```

### 2. 部署 Attu (Milvus GUI)
```
docker run -d --name milvus-gui  -p 8000:3000 -e MILVUS_URL=172.17.0.1:19530 zilliz/attu
```
- MILVUS_URL 不能设置为 localhost 或 127.0.0.1，因为 Milvus 是部署在 Docker 中，需要使用 172.17.0.1