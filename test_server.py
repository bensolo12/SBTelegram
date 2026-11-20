import unittest

from aiohttp.test_utils import TestClient, TestServer

from server import create_app


class SignalingServerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = TestClient(TestServer(create_app()))
        await self.client.start_server()

    async def asyncTearDown(self):
        await self.client.close()

    async def join_room(self, room_code):
        socket = await self.client.ws_connect("/signal")
        await socket.send_json({"type": "join", "room": room_code})
        return socket, await socket.receive_json()

    async def test_two_clients_exchange_peer_signals(self):
        first, first_join = await self.join_room("test-room-1")
        self.assertEqual(first_join, {
            "type": "joined",
            "room": "test-room-1",
            "initiator": True,
        })

        second, second_join = await self.join_room("test-room-1")
        self.assertEqual(second_join["type"], "joined")
        self.assertFalse(second_join["initiator"])
        self.assertEqual(await first.receive_json(), {"type": "peer-joined"})

        offer = {
            "kind": "description",
            "description": {"type": "offer", "sdp": "test SDP"},
        }
        await first.send_json({"type": "signal", "data": offer})
        self.assertEqual(await second.receive_json(), {"type": "signal", "data": offer})

        await first.close()
        self.assertEqual(await second.receive_json(), {"type": "peer-left"})
        await second.close()

    async def test_room_rejects_a_third_client(self):
        first, _ = await self.join_room("test-room-2")
        second, _ = await self.join_room("test-room-2")
        await first.receive_json()

        third, response = await self.join_room("test-room-2")
        self.assertEqual(response["type"], "error")
        self.assertIn("two clients", response["message"])

        await first.close()
        await second.close()
        await third.close()

    async def test_serves_the_web_client(self):
        response = await self.client.get("/")
        self.assertEqual(response.status, 200)
        self.assertIn("Connect two clients", await response.text())


if __name__ == "__main__":
    unittest.main()
