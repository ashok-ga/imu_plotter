import asyncio
import websockets

async def test_sender(websocket, path):
    print("✅ WebSocket client connected.")
    try:
        await websocket.send("hello from server")
        await asyncio.sleep(5)
        await websocket.close()
    except Exception as e:
        print(f"⚠️ Server crashed with error: {e}")

async def main():
    async with websockets.serve(test_sender, "0.0.0.0", 8000):
        print("🌐 WebSocket server running on ws://0.0.0.0:8000")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
