''' Tests for runpod.serverless.modules.rp_ping '''

import os
import importlib

from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, Mock

import aiohttp
from runpod.serverless.modules import rp_ping

class TestPing(IsolatedAsyncioTestCase):
    ''' Tests for rp_ping '''

    def test_variables(self):
        '''
        Tests that the variables are set correctly
        '''
        os.environ["RUNPOD_WEBHOOK_PING"] = "PING_NOT_SET"

        importlib.reload(rp_ping)

        self.assertEqual(rp_ping.PING_URL, "PING_NOT_SET")
        self.assertEqual(rp_ping.PING_INTERVAL, 10000)

        os.environ["RUNPOD_WEBHOOK_PING"] = "https://test.com/ping"
        os.environ["RUNPOD_PING_INTERVAL"] = "20000"

        importlib.reload(rp_ping)

        self.assertEqual(rp_ping.PING_URL, "https://test.com/ping")
        self.assertEqual(rp_ping.PING_INTERVAL, 20000)

    async def test_start_ping(self):
        '''
        Tests that the start_ping function works correctly
        '''
        os.environ["RUNPOD_WEBHOOK_PING"] = "https://test.com/ping"

        with patch("aiohttp.ClientSession.get") as mock_get:

            # Normal case
            mock_get.return_value = Mock(status_code=200)

            importlib.reload(rp_ping)
            new_ping = rp_ping.HeartbeatSender()

            mock_session = Mock()
            mock_session.headers.update = Mock()

            # Success case
            await new_ping._send_ping() # pylint: disable=protected-access

            rp_ping.PING_URL = "https://test.com/ping"

            self.assertEqual(rp_ping.PING_URL, "https://test.com/ping")

            # Exception case
            mock_get.side_effect = aiohttp.ClientError("Test Error")

            with patch("runpod.serverless.modules.rp_ping.log.error") as mock_log_error:
                await new_ping._send_ping() # pylint: disable=protected-access
                assert mock_log_error.call_count == 2