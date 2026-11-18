import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from fastapi import FastAPI
import uvicorn

app = FastAPI()

process_pool = ProcessPoolExecutor(max_workers=6)

def heavy_cpu_calculation(n: int):
    result = 0.0
    for i in range(1, n):
        result += i**0.5 * 3.1415926
    return f"CPU 任务计算完成，结果校验和：{result:.2f}"

@app.get("/api/task")
async def handle_request():
    start_time = time.time()
    # 模拟 I/O 密集型操作，比如访问数据库或外部 API
    await asyncio.sleep(0.5)
    io_end_time = time.time()

    # 模拟 CPU 密集型操作，比如复杂计算
    # 1000000000 主要消耗单进程worker计算时间，这里为了测试nginx的负载均衡效果，使用50000000，然单次任务1~3s
    # locust 压测时会频繁触发该接口，测试 nginx 的负载均衡效果
    cpu_result = await asyncio.get_event_loop().run_in_executor(process_pool, heavy_cpu_calculation, 50000000)
    end_time = time.time()

    return {
        "status": "success",
        "io_simulate_time_sec":f"{io_end_time - start_time:.2f}s",
        "total_time_sec": f"{end_time - start_time:.2f}s",
        "cpu_task_result": cpu_result
    }

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    uvicorn.run(app, host="127.0.0.1", port=port)