import concurrent.futures
import requests
import time

# 定义要发送的请求函数
def send_get_request(i, url = "http://127.0.0.1:8015/predict/resnet50"):
    response = requests.get(url)
    # 处理响应数据

# 创建线程池

if __name__ == "__main__":
    # 提交请求任务给线程池
    count = 1000
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        futures = [executor.submit(send_get_request, i) for i in range(count)]

        # 获取任务的结果
        for future in concurrent.futures.as_completed(futures):
            # 处理任务的结果
            result = future.result()
            # 进一步处理结果数据
            
    t1 = time.time()
    all_time = t1 - t0
    print("con = {}".format(count / (t1 - t0)))