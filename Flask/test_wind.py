#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WindPy测试脚本
用于测试Wind API的连接和数据获取功能
"""

import pandas as pd
import sys
import os
from datetime import datetime, timedelta

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入Wind服务
from services.wind_service import WindService

def test_connection():
    """测试Wind连接"""
    print("==== 测试Wind连接 ====")
    
    wind_service = WindService()
    if wind_service:
        print("WindPy服务初始化成功")
    else:
        print("WindPy服务初始化失败")
    
    print()

def test_historical_data():
    """测试获取历史行情数据"""
    print("==== 测试获取历史行情数据 ====")
    
    wind_service = WindService()
    
    # 设置查询参数
    code = '000001.SZ'  # 平安银行
    fields = 'open,high,low,close,volume'
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"获取 {code} 从 {start_date} 到 {end_date} 的 {fields} 数据")
    
    try:
        # 获取数据
        data = wind_service.get_historical_data(code, fields, start_date, end_date)
        
        # 打印结果
        print(f"获取到 {len(data['dates'])} 条数据:")
        
        # 转换为DataFrame展示
        df = pd.DataFrame(data['data'], index=data['dates'], columns=data['fields'])
        print(df.head(10))
        
        print("测试成功!")
    except Exception as e:
        print(f"测试失败: {str(e)}")
    
    print()

def test_multiple_stocks():
    """测试获取多只股票数据"""
    print("==== 测试获取多只股票数据 ====")
    
    wind_service = WindService()
    
    # 设置查询参数
    codes = ['000001.SZ', '600000.SH', '600036.SH']  # 平安银行，浦发银行，招商银行
    field = 'close'
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    
    print(f"获取 {codes} 从 {start_date} 到 {end_date} 的 {field} 数据")
    
    try:
        results = {}
        
        # 逐个获取数据
        for code in codes:
            data = wind_service.get_historical_data(code, field, start_date, end_date)
            results[code] = data
        
        # 打印结果
        for code, data in results.items():
            print(f"{code} 获取到 {len(data['dates'])} 条数据")
            df = pd.DataFrame(data['data'], index=data['dates'], columns=data['fields'])
            print(df.head(5))
            print()
        
        print("测试成功!")
    except Exception as e:
        print(f"测试失败: {str(e)}")
    
    print()

if __name__ == "__main__":
    print("开始WindPy服务测试...")
    
    # 运行测试
    test_connection()
    test_historical_data()
    test_multiple_stocks()
    
    print("WindPy服务测试完成!") 