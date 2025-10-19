"""WebSocket server utilities."""

from __future__ import annotations

from collections.abc import AsyncGenerator

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
