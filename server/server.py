import cv2
import asyncio
import websockets
import json

from ccstream import process_image_to_chars

DEFAULT_WIDTH, DEFAULT_HEIGHT = 164, 81
HOST, PORT = "0.0.0.0", 3415


async def send_frames(websocket):
    print("Starting webcam...")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if ret:
            processed, palette = process_image_to_chars(frame)

            payload = {
                "width": DEFAULT_WIDTH,
                "height": DEFAULT_HEIGHT,
                "spaces": " " * DEFAULT_WIDTH,
                "palette": palette,
                "data": processed
            }

            await websocket.send(json.dumps(payload))


async def main():
    async with websockets.serve(send_frames, HOST, PORT):
        await asyncio.Future()


asyncio.run(main())
