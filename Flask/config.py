#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Flask配置
DEBUG = True
SECRET_KEY = 'wind-flask-app-secret-key'

# WindPy配置
WIND_WAIT_TIME = 120  # Wind API命令超时时间(秒)

# 默认查询参数
DEFAULT_CODE = '000001.SZ'  # 平安银行
DEFAULT_START_DATE = '2023-01-01'
DEFAULT_END_DATE = '2023-12-31'
DEFAULT_FIELDS = 'open,high,low,close,volume' 