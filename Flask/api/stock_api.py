from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from services.wind_service import WindService

stock_api = Blueprint('stock_api', __name__)
wind_service = WindService()

@stock_api.route('/api/stock/kline', methods=['GET'])
def get_kline_data():
    try:
        # 获取请求参数
        code = request.args.get('code')
        timeframe = request.args.get('timeframe', 'D')  # 默认日线
        limit = int(request.args.get('limit', 100))     # 默认100条数据
        
        # 计算日期范围
        end_date = datetime.now().strftime('%Y-%m-%d')
        if timeframe == 'D':
            start_date = (datetime.now() - timedelta(days=limit)).strftime('%Y-%m-%d')
            options = "PriceAdj=F"  # 前复权
        elif timeframe == 'W':
            start_date = (datetime.now() - timedelta(weeks=limit)).strftime('%Y-%m-%d')
            options = "PriceAdj=F;Period=W"
        elif timeframe == 'M':
            start_date = (datetime.now() - timedelta(days=limit*30)).strftime('%Y-%m-%d')
            options = "PriceAdj=F;Period=M"
        else:
            # 分钟级别数据
            minutes = int(timeframe)
            start_date = (datetime.now() - timedelta(minutes=minutes*limit)).strftime('%Y-%m-%d')
            options = f"PriceAdj=F;Period={minutes}"
        
        # 获取数据
        fields = "open,high,low,close,volume"
        data = wind_service.get_historical_data(
            code=code,
            fields=fields,
            start_date=start_date,
            end_date=end_date,
            options=options
        )
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@stock_api.route('/api/stock/realtime', methods=['GET'])
def get_realtime_data():
    try:
        code = request.args.get('code')
        fields = "rt_last,rt_vol,rt_amt,rt_chg,rt_pct_chg"
        
        data = wind_service.get_realtime_data(
            codes=code,
            fields=fields
        )
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500 