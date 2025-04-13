from llama_index.core import PromptTemplate

# 定义提示模板字符串
template_str = """
你是一个Python工程师, 你擅长FastAPI, 现在我希望你可以负责 vectorbuild_api_async.py 的代码维护和更新工作

应该保证尽可能少的改动代码的前提下, 满足新功能或改动诉求.

vectorbuild_api_async.py 介绍:
---
vectorbuild_api_async.py 的主要职责是提供一种API调用来自动从数据库拉取数据,处理数据,并构建向量库的能力
vectorbuild_api_async.py文件,是一个知识库构建项目的主入口, 由llama-index作为架构, FastAPI提供网络服务.
vectorbuild_api_async.py可以从一个自定义的包vectorbuilder 中获取构建方法, 并将这些方法封装成异步的API函数

---

vectorbuild_api_async.py 全部代码:
```python
import asyncio
import json
import os
import uuid
from collections import defaultdict

from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter

from vectorbuilder.build_address_index import build as build_address_by_blocks_number
from vectorbuilder.build_blocks_index import build as build_blocks_by_block_number
from vectorbuilder.build_logs_index import build as build_logs_by_id
from vectorbuilder.build_web3_index import build as build_web3_by_text
from vectorbuilder.build_token_trade import build as build_token_trade_by_time
from vectorbuilder.build_oingeckoMarket_index import build as build_oingeckoMarket_by_length
from vectorbuilder.build_news_index import build as build_news_by_time

# 全局任务存储
tasks = {}  # {task_id: {status, result, error}}
locks = defaultdict(asyncio.Lock)  # 任务锁，避免竞态条件

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.environ.get('bianxieai_API_KEY')
llm = OpenAI(
    model="gpt-4o",
    api_key=api_key,
    api_base='https://api.bianxieai.com/v1',
    temperature=0.1,
)
embed_model = OpenAIEmbedding(api_key=api_key, api_base='https://api.bianxieai.com/v1')
Settings.embed_model = embed_model
Settings.llm = llm
Settings.text_splitter = SentenceSplitter(chunk_size=8000, chunk_overlap=50)

# Token authentication
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "123456":  # TODO: 更新token
        raise HTTPException(status_code=403, detail="Invalid or missing token")

@app.post("/build/address")
async def build_address(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(credentials)
    data = await request.json()
    block_number = data.get("block_number", -1)
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    async def run_build_address():
        try:
            result = await asyncio.get_running_loop().run_in_executor(
                None,
                build_address_by_blocks_number,
                block_number
            )
            async with locks[task_id]:
                tasks[task_id]["status"] = "success"
                tasks[task_id]["result"] = result
        except Exception as e:
            async with locks[task_id]:
                tasks[task_id]["status"] = "failed"
                tasks[task_id]["error"] = str(e)
    
    asyncio.create_task(run_build_address())
    
    return {"task_id": task_id}

@app.post("/build/blocks")
async def build_blocks(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(credentials)
    data = await request.json()
    start_block_number = data.get("start_block_number", -1)
    end_block_number = data.get("end_block_number", -1)
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    async def run_build_blocks():
        try:
            result = await asyncio.get_running_loop().run_in_executor(
                None,
                build_blocks_by_block_number,
                start_block_number,
                end_block_number
            )
            async with locks[task_id]:
                tasks[task_id]["status"] = "success"
                tasks[task_id]["result"] = result
        except Exception as e:
            async with locks[task_id]:
                tasks[task_id]["status"] = "failed"
                tasks[task_id]["error"] = str(e)
    
    asyncio.create_task(run_build_blocks())
    
    return {"task_id": task_id}

@app.post("/build/logs")
async def build_logs(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(credentials)
    data = await request.json()
    start_id = data.get("start_id", -1)
    end_id = data.get("end_id", -1)
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    async def run_build_logs():
        try:
            result = await asyncio.get_running_loop().run_in_executor(
                None,
                build_logs_by_id,
                start_id,
                end_id
            )
            async with locks[task_id]:
                tasks[task_id]["status"] = "success"
                tasks[task_id]["result"] = result
        except Exception as e:
            async with locks[task_id]:
                tasks[task_id]["status"] = "failed"
                tasks[task_id]["error"] = str(e)
    
    asyncio.create_task(run_build_logs())
    
    return {"task_id": task_id}

@app.post("/build/web3")
async def build_web3(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(credentials)
    data = await request.json()
    text = data.get("text", "")
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    async def run_build_web3():
        try:
            result = await asyncio.get_running_loop().run_in_executor(
                None,
                build_web3_by_text,
                text
            )
            async with locks[task_id]:
                tasks[task_id]["status"] = "success"
                tasks[task_id]["result"] = result
        except Exception as e:
            async with locks[task_id]:
                tasks[task_id]["status"] = "failed"
                tasks[task_id]["error"] = str(e)
    
    asyncio.create_task(run_build_web3())
    
    return {"task_id": task_id}

@app.post("/build/token_trade")
async def build_token_trade(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(credentials)
    data = await request.json()
    time_ = data.get("time", "")
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    async def run_build_token_trade():
        try:
            result = await asyncio.get_running_loop().run_in_executor(
                None,
                build_token_trade_by_time,
                time_
            )
            async with locks[task_id]:
                tasks[task_id]["status"] = "success"
                tasks[task_id]["result"] = result
        except Exception as e:
            async with locks[task_id]:
                tasks[task_id]["status"] = "failed"
                tasks[task_id]["error"] = str(e)
    
    asyncio.create_task(run_build_token_trade())
    
    return {"task_id": task_id}

@app.post("/build/oingecko_market")
async def build_oingecko_market(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(credentials)
    data = await request.json()
    length = data.get("length", 1000)
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    async def run_build_oingecko_market():
        try:
            result = await asyncio.get_running_loop().run_in_executor(
                None,
                build_oingeckoMarket_by_length,
                length
            )
            async with locks[task_id]:
                tasks[task_id]["status"] = "success"
                tasks[task_id]["result"] = result
        except Exception as e:
            async with locks[task_id]:
                tasks[task_id]["status"] = "failed"
                tasks[task_id]["error"] = str(e)
    
    asyncio.create_task(run_build_oingecko_market())
    
    return {"task_id": task_id}

@app.post("/build/news")
async def build_news(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(credentials)
    data = await request.json()
    start_time = data.get("start_time", "")
    end_time = data.get("end_time", None)
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    async def run_build_news():
        try:
            result = await asyncio.get_running_loop().run_in_executor(
                None,
                build_news_by_time,
                start_time,
                end_time
            )
            async with locks[task_id]:
                tasks[task_id]["status"] = "success"
                tasks[task_id]["result"] = result
        except Exception as e:
            async with locks[task_id]:
                tasks[task_id]["status"] = "failed"
                tasks[task_id]["error"] = str(e)
    
    asyncio.create_task(run_build_news())
    
    return {"task_id": task_id}

@app.get("/task/{task_id}")
async def get_task_status(task_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(credentials)
    
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    async with locks[task_id]:
        return {
            "task_id": task_id,
            "status": task["status"],
            "result": task["result"] if task["status"] == "success" else None,
            "error": task["error"] if task["status"] == "failed" else None
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

用户的代码片段和要求:
---
{prompt}
---
输出新的build函数:
"""

# 创建PromptTemplate实例
qa_template = PromptTemplate(template=template_str)

