export PATH=/root/miniconda3/envs/triton/bin/:$PATH
uvicorn fastapi_server:app --reload --port 8015