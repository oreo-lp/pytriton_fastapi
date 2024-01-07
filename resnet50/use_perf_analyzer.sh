
export LD_LIBRARY_PATH=/usr/local/cuda-12.2/lib64/:$LD_LIBRARY_PATH
export PATH=/root/miniconda3/envs/triton/bin/:$PATH

perf_analyzer -u 127.0.0.1:8000 \
  -i http \
  -m ResNet50 \
  --measurement-mode count_windows \
  --measurement-request-count 100 \
  --concurrency-range 64:64:64 \
  -v
