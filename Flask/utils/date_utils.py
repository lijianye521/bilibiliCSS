#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import pandas as pd

def validate_date_format(date_str):
    """
    验证日期格式是否有效
    
    Args:
        date_str (str): 日期字符串，如'2023-01-01'
        
    Returns:
        bool: 格式是否有效
    """
    try:
        # 尝试多种常见格式
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d']:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        return False
    except:
        return False

def standardize_date_format(date_str):
    """
    将日期字符串标准化为'YYYY-MM-DD'格式
    
    Args:
        date_str (str): 日期字符串，如'20230101'
        
    Returns:
        str: 标准化的日期字符串，如'2023-01-01'
    """
    try:
        # 尝试多种常见格式
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d']:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        return date_str
    except:
        return date_str

def get_previous_trading_days(end_date=None, days=30):
    """
    获取之前的交易日
    
    Args:
        end_date (str, optional): 结束日期，默认为今天
        days (int, optional): 交易日数量，默认为30
        
    Returns:
        list: 交易日列表
    """
    # 注意：这个函数在实际使用中应该使用WindPy的w.tdays来获取真实的交易日
    # 这里简化处理，假设周一至周五都是交易日
    
    if end_date:
        end_dt = datetime.strptime(standardize_date_format(end_date), '%Y-%m-%d')
    else:
        end_dt = datetime.now()
    
    result = []
    current_dt = end_dt
    
    while len(result) < days:
        # 跳过周六和周日
        if current_dt.weekday() < 5:  # 0-4表示周一至周五
            result.append(current_dt.strftime('%Y-%m-%d'))
        
        current_dt -= timedelta(days=1)
    
    # 按日期升序排序
    result.reverse()
    
    return result

def calculate_date_range(start_date, end_date):
    """
    计算两个日期之间的天数
    
    Args:
        start_date (str): 开始日期
        end_date (str): 结束日期
        
    Returns:
        int: 天数
    """
    start_dt = datetime.strptime(standardize_date_format(start_date), '%Y-%m-%d')
    end_dt = datetime.strptime(standardize_date_format(end_date), '%Y-%m-%d')
    
    delta = end_dt - start_dt
    
    return delta.days + 1  # 包含开始和结束日期 