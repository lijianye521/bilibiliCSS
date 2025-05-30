import unittest
import json
from app import app
from services.wind_service import WindService
from unittest.mock import patch

class TestWindAPI(unittest.TestCase):
    def setUp(self):
        """测试前的设置"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """测试健康检查接口"""
        response = self.app.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'running')
        self.assertIn('wind_connected', data)

    @patch('services.wind_service.WindService.get_historical_data')
    def test_get_historical_data(self, mock_get_historical):
        """测试获取历史数据接口"""
        # 模拟返回数据
        mock_data = {
            'dates': ['2023-01-01', '2023-01-02'],
            'fields': ['open', 'close'],
            'data': [[10.0, 11.0], [11.0, 12.0]]
        }
        mock_get_historical.return_value = mock_data

        # 测试默认参数
        response = self.app.get('/api/historical')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data'], mock_data)

        # 测试自定义参数
        response = self.app.get('/api/historical?code=600000.SH&start_date=2024-01-01&end_date=2024-01-31')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    @patch('services.wind_service.WindService.get_realtime_data')
    def test_get_realtime_data(self, mock_get_realtime):
        """测试获取实时数据接口"""
        # 模拟返回数据
        mock_data = {
            'codes': ['000001.SZ'],
            'fields': ['rt_last', 'rt_vol'],
            'data': [[15.5, 1000000]]
        }
        mock_get_realtime.return_value = mock_data

        # 测试默认参数
        response = self.app.get('/api/realtime')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data'], mock_data)

        # 测试自定义参数
        response = self.app.get('/api/realtime?codes=600000.SH,000001.SZ&fields=rt_last')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_handling(self):
        """测试错误处理"""
        # 测试无效的股票代码
        response = self.app.get('/api/historical?code=invalid_code')
        self.assertEqual(response.status_code, 500)

        response = self.app.get('/api/realtime?codes=invalid_code')
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main() 