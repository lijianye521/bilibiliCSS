#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime

class MarketData:
    """市场数据模型类"""
    
    def __init__(self, data=None):
        """
        初始化市场数据模型
        
        Args:
            data (dict, optional): 原始数据字典
        """
        self.data = data if data else {}
        self.df = None
        
        # 如果有数据，转换为DataFrame
        if data and 'dates' in data and 'fields' in data and 'data' in data:
            self._convert_to_dataframe()
    
    def _convert_to_dataframe(self):
        """将原始数据转换为DataFrame"""
        if not self.data:
            return
        
        # 创建DataFrame
        df = pd.DataFrame(
            self.data['data'],
            index=self.data['dates'],
            columns=self.data['fields']
        )
        
        # 转换索引为日期类型
        df.index = pd.to_datetime(df.index)
        
        self.df = df
    
    def to_dict(self):
        """将数据转换为字典格式"""
        if self.df is None:
            return self.data
        
        return {
            'dates': self.df.index.strftime('%Y-%m-%d').tolist(),
            'fields': self.df.columns.tolist(),
            'data': self.df.values.tolist()
        }
    
    def to_json(self):
        """将数据转换为JSON格式"""
        if self.df is None:
            return {}
        
        # 将日期索引转换为列
        df_reset = self.df.reset_index()
        df_reset.rename(columns={'index': 'date'}, inplace=True)
        df_reset['date'] = df_reset['date'].dt.strftime('%Y-%m-%d')
        
        # 将DataFrame转为记录列表
        return df_reset.to_dict(orient='records')
    
    def filter_by_date_range(self, start_date=None, end_date=None):
        """
        按日期范围过滤数据
        
        Args:
            start_date (str, optional): 开始日期
            end_date (str, optional): 结束日期
            
        Returns:
            MarketData: 过滤后的市场数据对象
        """
        if self.df is None:
            return self
        
        df_copy = self.df.copy()
        
        if start_date:
            start_date = pd.to_datetime(start_date)
            df_copy = df_copy[df_copy.index >= start_date]
        
        if end_date:
            end_date = pd.to_datetime(end_date)
            df_copy = df_copy[df_copy.index <= end_date]
        
        # 创建新的市场数据对象
        filtered_data = MarketData()
        filtered_data.df = df_copy
        
        return filtered_data
    
    def calculate_returns(self, price_column='close'):
        """
        计算收益率
        
        Args:
            price_column (str): 价格列名，默认为'close'
            
        Returns:
            pandas.Series: 收益率序列
        """
        if self.df is None or price_column not in self.df.columns:
            return None
        
        # 计算日收益率
        returns = self.df[price_column].pct_change()
        
        return returns
    
    @staticmethod
    def combine_data(data_list):
        """
        合并多个市场数据对象
        
        Args:
            data_list (list): MarketData对象列表
            
        Returns:
            pandas.DataFrame: 合并后的DataFrame
        """
        if not data_list:
            return None
        
        dfs = [data.df for data in data_list if data.df is not None]
        
        if not dfs:
            return None
        
        # 合并多个DataFrame
        combined_df = pd.concat(dfs, axis=1)
        
        return combined_df 