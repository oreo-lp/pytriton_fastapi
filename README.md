# pytriton_fastapi
基于pytriton对模型进行封装，并对triton client端使用fastapi进行微服务封装，供外部客户端进行接口的调用。本项目将主要对resnet50和bert模型进行测试，测试torch、onnx、trt等框架的并发性。  
cuda12.2   

## 1. ResNet50模型
### 1.1 perf_analyzer 
使用perf_analyzer工具分析triton server的并发性和时延性  
前提：设置的triton的最大并发为64  
执行脚本：
```bash
sh use_perf_analyzer.sh
```
| model | 时延(ms) | 吞吐量(infer/sec) | 
| --- | --- | ---| 
| ins-1-bs1 | 1155 | 54 |  
| ins-1-bs2 | 498 | 128 |  
| ins-1-bs4| 271 |  233 |  
| ins-1-bs8 | 165 |  370 |  
| ins-1-bs16 | 119 | 523 |  
| ins-1-bs32 | 107 | 596 |   
| ins-1-bs64 | 101 | 628 |  
从上的实验结果可以发现，拼batch可以增加模型的吞吐量！ 
当bs设置为64的时候， triton server的推理bs基本上都拼不到64了，因此下文针对bs=32的时候，测试不同instance的推理效率。  

| model | 时延(ms) | 吞吐量(infer/sec) | 
| --- | --- | ---| 
| ins-1-bs32 | 107| 596 |
| ins-2-bs32 | 79| 812 | 
| ins-4-bs32 | 117 | 542 |   
从上面的实验结果也能发现，增加模型实例也可以增加模型的吞吐量  
但是盲目增加实例个数并不一定能提高吞吐量，一定要根据需求来配置实例个数。  
### 1.2 使用fastapi测试
并发发送1000条请求，测试请求的吞吐量
| model | 吞吐量(infer/sec) | 
| --- | --- | 
| ins-1-bs1 | 50 |  
| ins-1-bs2 | 101 |  
| ins-1-bs4 | 195 | 
| ins-1-bs8 | 208 |     
| ins-1-bs16 | 204 |   

(1) 当bs=8的时候，triton server的拼的bs就已经不足8了；  
(2) fastapi的效率较perf的吞吐量低的主要原因就是perf是主要测试triton server的效率，即主要测试模型推理的吞吐量；  
(3) 而fastapi则是测试数据预处理+模型推理的效率，需要CPU+GPU的计算，因此有一定的推理损耗。  
下面测试一下bs=8的前提下，不同instance的效率：  

| model | 吞吐量(infer/sec) | 
| --- | --- | 
| ins-1-bs8 | 208 |  
| ins-2-bs8 | 207 |  
| ins-4-bs8 | 187 |  

## 2. BERT模型
