#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, render_template
from services.wind_service import WindService
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 创建Blueprint
market_data = Blueprint('market_data', __name__)

# 初始化Wind服务
wind_service = WindService()

@market_data.route('/historical', methods=['GET'])
def get_historical_data():
    """获取历史行情数据"""
    try:
        # 获取请求参数
        code = request.args.get('code', '000001.SZ')
        start_date = request.args.get('start_date', '2023-01-01')
        end_date = request.args.get('end_date', '2023-12-31')
        fields = request.args.get('fields', 'open,high,low,close,volume')
        options = request.args.get('options', '')
        
        # 调用Wind服务获取数据
        data = wind_service.get_historical_data(code, fields, start_date, end_date, options)
        
        return jsonify({
            'success': True,
            'data': data,
            'message': f'成功获取{code}从{start_date}到{end_date}的历史数据'
        })
    
    except Exception as e:
        logger.error(f"获取历史数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取历史数据失败: {str(e)}'
        }), 500

@market_data.route('/realtime', methods=['GET'])
def get_realtime_data():
    """获取实时行情数据"""
    try:
        # 获取请求参数
        codes = request.args.get('codes', '000001.SZ')
        fields = request.args.get('fields', 'rt_last,rt_vol,rt_amt')
        
        # 调用Wind服务获取数据
        data = wind_service.get_realtime_data(codes, fields)
        
        return jsonify({
            'success': True,
            'data': data,
            'message': f'成功获取{codes}的实时数据'
        })
    
    except Exception as e:
        logger.error(f"获取实时数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取实时数据失败: {str(e)}'
        }), 500

@market_data.route('/dashboard')
def dashboard():
    """数据展示仪表盘"""
    return render_template('dashboard.html') 