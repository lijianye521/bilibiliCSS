#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from services.wind_service import WindService
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')

# 初始化Wind服务
wind_service = WindService()

@app.route('/api/historical', methods=['GET'])
def get_historical_data():
    """获取历史行情数据API"""
    try:
        code = request.args.get('code', '000001.SZ')  # 默认获取平安银行
        start_date = request.args.get('start_date', '2023-01-01')
        end_date = request.args.get('end_date', '2023-12-31')
        fields = request.args.get('fields', 'open,high,low,close,volume')
        options = request.args.get('options', '')
        
        data = wind_service.get_historical_data(code, fields, start_date, end_date, options)
        return jsonify({
            'success': True, 
            'data': data,
            'message': f'成功获取{code}从{start_date}到{end_date}的历史数据'
        })
    except Exception as e:
        logger.error(f"获取历史数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/realtime', methods=['GET'])
def get_realtime_data():
    """获取实时行情数据API"""
    try:
        codes = request.args.get('codes', '000001.SZ')
        fields = request.args.get('fields', 'rt_last,rt_vol,rt_amt')
        
        data = wind_service.get_realtime_data(codes, fields)
        return jsonify({
            'success': True, 
            'data': data,
            'message': f'成功获取{codes}的实时数据'
        })
    except Exception as e:
        logger.error(f"获取实时数据失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查API"""
    try:
        is_connected = wind_service.check_connection() if hasattr(wind_service, 'check_connection') else True
        return jsonify({
            'success': True,
            'status': 'running',
            'wind_connected': is_connected
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 打印测试数据
    print("测试WindPy获取历史行情数据:")
    try:
        test_data = wind_service.get_historical_data('000001.SZ', 'open,high,low,close', '2023-01-01', '2023-01-10')
        print("获取数据成功:")
        print(f"日期: {test_data['dates'][:3]}...")
        print(f"字段: {test_data['fields']}")
        print(f"数据样本: {test_data['data'][:3]}...")
    except Exception as e:
        print(f"测试获取数据失败: {str(e)}")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 