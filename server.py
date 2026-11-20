import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

from aiohttp import WSMsgType, web


ROOM_CODE_PATTERN = re.compile(r"[A-Za-z0-9_-]{8,64}")
MAX_SIGNAL_MESSAGE_SIZE = 128 * 1024
INDEX_FILE = Path(__file__).with_name("index.html")
ROOMS_KEY = web.AppKey("rooms", dict)


async def serve_index(_request):
    return web.FileResponse(INDEX_FILE)


async def send_error(socket, message):
    await socket.send_json({"type": "error", "message": message})
    await socket.close()


async def signal(request):
    origin = request.headers.get("Origin")
    if origin and urlsplit(origin).netloc.lower() != request.host.lower():
        raise web.HTTPForbidden(text="Cross-origin signaling requests are not allowed.")

    socket = web.WebSocketResponse(
        heartbeat=30,
        max_msg_size=MAX_SIGNAL_MESSAGE_SIZE,
    )
    await socket.prepare(request)

    rooms = request.app[ROOMS_KEY]
    room_code = None
    try:
        async for message in socket:
            if message.type == WSMsgType.TEXT:
                try:
                    data = json.loads(message.data)
                except json.JSONDecodeError:
                    await send_error(socket, "Signaling messages must be valid JSON.")
                    break

                if not isinstance(data, dict):
                    await send_error(socket, "Signaling messages must be JSON objects.")
                    break

                if room_code is None:
                    proposed_code = data.get("room")
                    if data.get("type") != "join" or not isinstance(proposed_code, str):
                        await send_error(socket, "Join a room before sending signaling data.")
                        break
                    if not ROOM_CODE_PATTERN.fullmatch(proposed_code):
                        await send_error(socket, "Room codes must contain 8–64 letters, numbers, hyphens, or underscores.")
                        break

                    members = rooms.setdefault(proposed_code, set())
                    if len(members) >= 2:
                        await send_error(socket, "That room already has two clients.")
                        break

                    room_code = proposed_code
                    is_initiator = not members
                    members.add(socket)
                    await socket.send_json({
                        "type": "joined",
                        "room": room_code,
                        "initiator": is_initiator,
                    })
                    if not is_initiator:
                        for peer in tuple(members):
                            if peer is not socket and not peer.closed:
                                await peer.send_json({"type": "peer-joined"})
                    continue

                if data.get("type") != "signal":
                    await send_error(socket, "Only peer connection signaling is accepted after joining.")
                    break

                signal_data = data.get("data")
                if not isinstance(signal_data, dict):
                    await send_error(socket, "The peer connection details are invalid.")
                    break
                if signal_data.get("kind") == "description":
                    description = signal_data.get("description")
                    if (
                        not isinstance(description, dict)
                        or description.get("type") not in {"offer", "answer"}
                        or not isinstance(description.get("sdp"), str)
                    ):
                        await send_error(socket, "The peer connection description is invalid.")
                        break
                elif signal_data.get("kind") == "candidate":
                    candidate = signal_data.get("candidate")
                    if not isinstance(candidate, dict) or not isinstance(candidate.get("candidate"), str):
                        await send_error(socket, "The peer connection candidate is invalid.")
                        break
                else:
                    await send_error(socket, "The peer connection signal type is unsupported.")
                    break

                peers = [
                    peer for peer in rooms.get(room_code, ())
                    if peer is not socket and not peer.closed
                ]
                if not peers:
                    await send_error(socket, "No other client is connected to that room.")
                    break
                await peers[0].send_json({"type": "signal", "data": signal_data})

            elif message.type == WSMsgType.ERROR:
                request.app.logger.warning("Signaling WebSocket error: %s", socket.exception())
                break
    finally:
        if room_code is not None:
            members = rooms.get(room_code)
            if members is not None:
                members.discard(socket)
                for peer in tuple(members):
                    if not peer.closed:
                        try:
                            await peer.send_json({"type": "peer-left"})
                        except ConnectionError:
                            request.app.logger.info("A room client disconnected during notification.")
                if not members:
                    rooms.pop(room_code, None)

    return socket


def create_app():
    app = web.Application()
    app[ROOMS_KEY] = {}
    app.router.add_get("/", serve_index)
    app.router.add_get("/signal", signal)
    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
    )
