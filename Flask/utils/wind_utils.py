#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WindPy工具函数模块
提供常用的Wind数据获取和处理功能
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# 导入WindPy
try:
    from WindPy import w
except ImportError:
    raise ImportError("无法导入WindPy模块，请确保Wind Python API已正确安装")

# 配置日志
logger = logging.getLogger(__name__)

def get_trading_days(start_date, end_date=None, exchange='SSE'):
    """
    获取交易日列表
    
    Args:
        start_date (str): 开始日期
        end_date (str, optional): 结束日期，默认为当前日期
        exchange (str, optional): 交易所代码，默认为'SSE'(上海证券交易所)
        
    Returns:
        list: 交易日列表
    """
    try:
        # 如果未提供结束日期，使用当前日期
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        # 调用Wind API获取交易日
        result = w.tdays(start_date, end_date, f"TradingCalendar={exchange}")
        
        # 检查返回结果
        if result.ErrorCode != 0:
            logger.error(f"获取交易日失败: {result.ErrorCode}")
            return []
            
        # 转换为日期字符串列表
        trading_days = [d.strftime('%Y-%m-%d') for d in result.Data[0]]
        return trading_days
    
    except Exception as e:
        logger.error(f"获取交易日异常: {str(e)}")
        return []

def get_index_constituents(index_code, date=None):
    """
    获取指数成分股
    
    Args:
        index_code (str): 指数代码，如'000300.SH'(沪深300)
        date (str, optional): 查询日期，默认为当前日期
        
    Returns:
        list: 成分股代码列表
    """
    try:
        # 如果未提供日期，使用当前日期
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
            
        # 调用Wind API获取指数成分股
        result = w.wset("indexconstituent", f"date={date};windcode={index_code}")
        
        # 检查返回结果
        if result.ErrorCode != 0:
            logger.error(f"获取指数成分股失败: {result.ErrorCode}")
            return []
            
        # 获取成分股代码
        constituents = result.Data[1]  # 第2列是成分股代码
        return constituents
    
    except Exception as e:
        logger.error(f"获取指数成分股异常: {str(e)}")
        return []

def calculate_technical_indicators(price_data, ma_periods=[5, 10, 20, 60]):
    """
    计算技术指标
    
    Args:
        price_data (pandas.DataFrame): 价格数据，包含'close'列
        ma_periods (list, optional): 移动平均周期列表
        
    Returns:
        pandas.DataFrame: 添加技术指标后的数据
    """
    try:
        # 复制数据以避免修改原始数据
        df = price_data.copy()
        
        # 确保数据包含'close'列
        if 'close' not in df.columns:
            logger.error("价格数据中缺少'close'列")
            return df
            
        # 计算移动平均线
        for period in ma_periods:
            df[f'ma{period}'] = df['close'].rolling(window=period).mean()
            
        # 计算MACD
        # 快速EMA通常为12日
        fast_ema = df['close'].ewm(span=12, adjust=False).mean()
        # 慢速EMA通常为26日
        slow_ema = df['close'].ewm(span=26, adjust=False).mean()
        # MACD线 = 快速EMA - 慢速EMA
        df['macd'] = fast_ema - slow_ema
        # 信号线通常为MACD的9日EMA
        df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        # MACD柱状图 = MACD线 - 信号线
        df['macd_hist'] = df['macd'] - df['signal']
            
        # 计算RSI (14日RSI)
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))
            
        # 计算布林带 (20日布林带)
        df['boll_mid'] = df['close'].rolling(window=20).mean()
        df['boll_std'] = df['close'].rolling(window=20).std()
        df['boll_upper'] = df['boll_mid'] + (df['boll_std'] * 2)
        df['boll_lower'] = df['boll_mid'] - (df['boll_std'] * 2)
            
        return df
    
    except Exception as e:
        logger.error(f"计算技术指标异常: {str(e)}")
        return price_data

def get_fundamental_data(codes, fields, date=None):
    """
    获取基本面数据
    
    Args:
        codes (str or list): 证券代码，如'000001.SZ'或['000001.SZ', '600000.SH']
        fields (str or list): 字段列表，如'pe_ttm,pb,ps_ttm'
        date (str, optional): 查询日期，默认为当前日期
        
    Returns:
        pandas.DataFrame: 基本面数据
    """
    try:
        # 如果未提供日期，使用当前日期
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
            
        # 调用Wind API获取基本面数据
        result = w.wss(codes, fields, f"tradeDate={date}")
        
        # 检查返回结果
        if result.ErrorCode != 0:
            logger.error(f"获取基本面数据失败: {result.ErrorCode}")
            return pd.DataFrame()
            
        # 将结果转换为DataFrame
        df = pd.DataFrame(result.Data, index=result.Fields, columns=result.Codes).T
        return df
    
    except Exception as e:
        logger.error(f"获取基本面数据异常: {str(e)}")
        return pd.DataFrame()

def get_industry_classification(codes, classification_standard='sw'):
    """
    获取行业分类
    
    Args:
        codes (str or list): 证券代码，如'000001.SZ'或['000001.SZ', '600000.SH']
        classification_standard (str, optional): 行业分类标准，默认为'sw'(申万)
        
    Returns:
        pandas.DataFrame: 行业分类数据
    """
    try:
        # 根据分类标准设置options
        classification_map = {
            'sw': 'industryType=1',  # 申万行业分类
            'wind': 'industryType=2',  # Wind行业分类
            'cics': 'industryType=3'  # 中信行业分类
        }
        
        options = classification_map.get(classification_standard.lower(), 'industryType=1')
        
        # 调用Wind API获取行业分类
        result = w.wss(codes, "industry_sw", options)
        
        # 检查返回结果
        if result.ErrorCode != 0:
            logger.error(f"获取行业分类失败: {result.ErrorCode}")
            return pd.DataFrame()
            
        # 将结果转换为DataFrame
        df = pd.DataFrame({
            'code': result.Codes,
            'industry': result.Data[0]
        })
        
        return df
    
    except Exception as e:
        logger.error(f"获取行业分类异常: {str(e)}")
        return pd.DataFrame() 