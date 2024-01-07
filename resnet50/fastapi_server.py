from fastapi import FastAPI
import torch
from pytriton.client import AsyncioModelClient
import numpy as np
import torch



config_client = AsyncioModelClient("localhost", "ResNet50")

app = FastAPI()

@app.get("/predict/resnet50")
async def predict():
    input1_batch = torch.randn(1, 3, 224, 224).cpu().detach().numpy()
    input1_batch = input1_batch.astype(np.float16)

    result_dict = await config_client.infer_batch(input1_batch)
    
    print("result_dict = {}".format(result_dict))
    # Return the result dictionary as JSON
    return {"status":"success"}

    
# 启动fastapi server的脚本
# fastapi_server必须是本py脚本的名字
# uvicorn fastapi_server:app --reload --port 8015