#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wind API服务启动脚本
"""

import os
import sys
import logging
from app import app

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('wind_api.log')
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 5000))
        host = os.environ.get("HOST", "0.0.0.0")
        debug = os.environ.get("DEBUG", "True").lower() == "true"
        
        logger.info(f"启动Wind API服务，地址: http://{host}:{port}")
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        logger.error(f"启动服务失败: {str(e)}")
        sys.exit(1) 