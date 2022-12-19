''' Tests for runpod | serverless| modules | pod_worker.py '''

import unittest
from unittest.mock import patch, mock_open

from runpod.serverless.modules import pod_worker


class TestPodWorker(unittest.TestCase):
    ''' Tests for pod_worker '''

    @patch('runpod.serverless.modules.lifecycle')
    def test_start_worker(self, mock_lifecycle):
        '''
        Tests start_worker
        '''
        pod_worker.start_worker()
        mock_lifecycle.LifecycleManager.assert_called_once_with()