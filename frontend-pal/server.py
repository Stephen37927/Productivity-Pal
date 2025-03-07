import asyncio 
import websockets
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from oscopilot.agents.task_schedule_agent import TaskScheduleAgent

agent=TaskScheduleAgent()

async def handle_websocket(websocket):  # 添加 path 参数
    try:
        async for message in websocket:
            data = json.loads(message)
            dueDate=data['dueDate']+" 23:59:59"
            print(dueDate)
            agent.schedule_task(3, data['name'], data['description'], dueDate)
            print("收到任务数据:")
            print(f"任务名: {data['name']}")
            print(f"任务描述: {data['description']}")
            print(f"截止日期: {data['dueDate']}")
            print(f"提醒时间: {data['reDate']}")

            
            # 发送确认消息给客户端
            await websocket.send(json.dumps({"status": "success"}))
    except Exception as e:
        print(f"处理消息时出错: {e}")

async def main():
    print("WebSocket 服务器已启动，等待连接...")
    async with websockets.serve(handle_websocket, "localhost", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止")