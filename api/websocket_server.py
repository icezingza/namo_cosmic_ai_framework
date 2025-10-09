"""WebSocket server utilities."""

from __future__ import annotations

import asyncio
from typing import AsyncGenerator

from fastapi import WebSocket


async def echo_stream(websocket: WebSocket) -> AsyncGenerator[str, None]:
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"echo: {message}")
            yield message
    except Exception:
        await websocket.close()
        return
