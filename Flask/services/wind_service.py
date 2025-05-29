#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import traceback
import logging
from functools import wraps

# 导入WindPy
try:
    from WindPy import w
except ImportError:
    raise ImportError("无法导入WindPy模块，请确保Wind Python API已正确安装")

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def wind_decorator(func):
    """Wind API装饰器，用于处理连接和错误"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # 检查WindPy是否已连接
            if not w.isconnected():
                logger.info("WindPy未连接，正在尝试连接...")
                result = w.start()
                if result.ErrorCode != 0:
                    raise Exception(f"WindPy连接失败: {result.ErrorCode}")
                logger.info("WindPy连接成功")
            
            # 执行被装饰的函数
            return func(*args, **kwargs)
        
        except Exception as e:
            logger.error(f"WindPy操作失败: {str(e)}")
            logger.error(traceback.format_exc())
            # 尝试关闭连接
            try:
                w.stop()
            except:
                pass
            # 重新抛出异常
            raise
    
    return wrapper

class WindService:
    """Wind数据服务类"""
    
    def __init__(self, wait_time=120):
        """
        初始化Wind服务
        
        Args:
            wait_time (int): API超时时间(秒)
        """
        self.wait_time = wait_time
        # 尝试启动WindPy
        try:
            if not w.isconnected():
                result = w.start(waitTime=self.wait_time)
                if result.ErrorCode != 0:
                    logger.error(f"WindPy启动失败: {result.ErrorCode}")
                else:
                    logger.info("WindPy启动成功")
        except Exception as e:
            logger.error(f"WindPy初始化失败: {str(e)}")
    
    def __del__(self):
        """析构函数，确保关闭Wind连接"""
        try:
            if w.isconnected():
                w.stop()
                logger.info("WindPy连接已关闭")
        except:
            pass
    
    def check_connection(self):
        """
        检查WindPy连接状态
        
        Returns:
            bool: 是否连接成功
        """
        try:
            return w.isconnected()
        except Exception as e:
            logger.error(f"检查WindPy连接失败: {str(e)}")
            return False
    
    @wind_decorator
    def get_historical_data(self, code, fields, start_date, end_date, options=""):
        """
        获取历史行情数据
        
        Args:
            code (str): 证券代码，如'000001.SZ'
            fields (str): 字段列表，如'open,high,low,close,volume'
            start_date (str): 开始日期，如'2023-01-01'
            end_date (str): 结束日期，如'2023-12-31'
            options (str, optional): 额外选项，如'PriceAdj=F'前复权
        
        Returns:
            dict: 包含历史数据的字典
        """
        logger.info(f"获取{code}从{start_date}到{end_date}的{fields}数据")
        
        # 调用Wind API获取数据
        result = w.wsd(code, fields, start_date, end_date, options, usedf=True)
        
        # 检查返回结果
        if result[0] != 0:
            error_msg = f"获取数据失败，错误码: {result[0]}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # 获取DataFrame结果
        df = result[1]
        
        # 转换日期格式并设置为索引
        if not df.empty:
            # 确保索引是日期格式
            if not isinstance(df.index, pd.DatetimeIndex):
                df.index = pd.to_datetime(df.index)
            
            # 格式化日期为字符串
            df.index = df.index.strftime('%Y-%m-%d')
        
        # 转换为字典格式
        data = {
            'dates': df.index.tolist(),
            'fields': df.columns.tolist(),
            'data': df.values.tolist()
        }
        
        return data
    
    @wind_decorator
    def get_realtime_data(self, codes, fields):
        """
        获取实时行情数据
        
        Args:
            codes (str): 证券代码，如'000001.SZ,600000.SH'
            fields (str): 字段列表，如'rt_last,rt_vol'
            
        Returns:
            dict: 包含实时数据的字典
        """
        logger.info(f"获取{codes}的实时{fields}数据")
        
        # 调用Wind API获取数据
        result = w.wsq(codes, fields, usedf=True)
        
        # 检查返回结果
        if result[0] != 0:
            error_msg = f"获取实时数据失败，错误码: {result[0]}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # 获取DataFrame结果
        df = result[1]
        
        # 转换为字典格式
        data = {
            'codes': df.index.tolist(),
            'fields': df.columns.tolist(),
            'data': df.values.tolist()
        }
        
        return data 