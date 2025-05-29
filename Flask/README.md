# Wind金融数据API服务

这是一个基于Flask和WindPy的金融数据API服务，提供历史行情数据和实时行情数据的获取接口。

## 环境要求

- Python 3.6+
- Wind金融终端（已安装并激活）
- WindPy Python API

## 安装步骤

1. 安装Wind金融终端并激活
2. 安装项目依赖
   ```bash
   pip install -r requirements.txt
   ```
3. 安装WindPy（参考Wind官方文档）

## 启动服务

```bash
python app.py
```

服务默认运行在 `http://0.0.0.0:5000`

## API接口说明

### 1. 获取历史行情数据

**接口**: `/api/historical`

**方法**: GET

**参数**:
- `code`: 证券代码，如 "000001.SZ"（默认为平安银行）
- `start_date`: 开始日期，格式为 "YYYY-MM-DD"（默认为"2023-01-01"）
- `end_date`: 结束日期，格式为 "YYYY-MM-DD"（默认为"2023-12-31"）
- `fields`: 字段列表，用逗号分隔，如 "open,high,low,close,volume"
- `options`: 额外选项，如 "PriceAdj=F"（前复权）

**返回示例**:
```json
{
  "success": true,
  "data": {
    "dates": ["2023-01-01", "2023-01-02", "..."],
    "fields": ["open", "high", "low", "close", "volume"],
    "data": [[12.5, 13.1, 12.4, 12.9, 123456], [...]]
  },
  "message": "成功获取000001.SZ从2023-01-01到2023-12-31的历史数据"
}
```

### 2. 获取实时行情数据

**接口**: `/api/realtime`

**方法**: GET

**参数**:
- `codes`: 证券代码，用逗号分隔，如 "000001.SZ,600000.SH"
- `fields`: 字段列表，用逗号分隔，如 "rt_last,rt_vol,rt_amt"

**返回示例**:
```json
{
  "success": true,
  "data": {
    "codes": ["000001.SZ", "600000.SH"],
    "fields": ["rt_last", "rt_vol", "rt_amt"],
    "data": [[12.5, 123456, 1543200], [...]]
  },
  "message": "成功获取000001.SZ,600000.SH的实时数据"
}
```

### 3. 健康检查

**接口**: `/api/health`

**方法**: GET

**返回示例**:
```json
{
  "success": true,
  "status": "running",
  "wind_connected": true
}
```

## 注意事项

- 使用前确保Wind金融终端已启动并登录
- WindPy API需要单独安装，不能通过pip安装
- 本服务为纯后端API服务，不提供前端界面 