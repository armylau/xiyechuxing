"""微信支付模块"""

import time
import uuid
from datetime import datetime, timedelta
from typing import Any

# 微信支付配置（请替换为你的真实配置）
WECHAT_PAY_CONFIG = {
    "mchid": "YOUR_MCHID",  # 商户号
    "api_key": "YOUR_API_KEY",  # API密钥
    "appid": "YOUR_APPID",  # 小程序AppID
    "notify_url": "https://your-domain.com/api/payment/notify",  # 支付结果通知URL
}


def generate_nonce_str() -> str:
    """生成随机字符串"""
    return uuid.uuid4().hex[:32]


def generate_out_trade_no() -> str:
    """生成商户订单号"""
    return f"TK{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"


def create_payment_order(order_data: dict[str, Any]) -> dict[str, Any]:
    """
    创建微信支付订单
    
    实际项目中应该：
    1. 调用微信统一下单 API
    2. 使用 wechatpayv3 库进行签名
    3. 保存订单到数据库
    
    这里提供模拟实现，方便测试
    """
    # 生成订单号
    out_trade_no = generate_out_trade_no()
    
    # 构建支付参数
    # 实际项目中这里应该调用微信支付统一下单接口
    # 返回 prepay_id 等参数
    
    # 模拟支付参数（实际项目中替换为真实微信支付返回）
    time_stamp = str(int(time.time()))
    nonce_str = generate_nonce_str()
    
    # 构建前端调起支付所需的参数
    pay_params = {
        "timeStamp": time_stamp,
        "nonceStr": nonce_str,
        "package": f"prepay_id=wx{uuid.uuid4().hex[:28]}",  # 实际应为微信返回的 prepay_id
        "signType": "RSA",  # 微信支付V3使用RSA签名
        "paySign": "",  # 实际应为服务端计算的签名
    }
    
    return {
        "code": 0,
        "data": {
            "out_trade_no": out_trade_no,
            "pay_params": pay_params,
            "total_fee": order_data.get("total_price", 0),
        },
        "msg": "支付订单创建成功"
    }


def verify_payment_result(notify_data: dict[str, Any]) -> bool:
    """
    验证微信支付回调通知
    实际项目中需要验证签名
    """
    # 实际项目中应该：
    # 1. 验证微信支付的签名
    # 2. 检查订单金额是否一致
    # 3. 更新订单状态
    return True


# 简易版支付实现（无需真实微信支付，适合演示/测试）
def create_mock_payment(order_data: dict[str, Any]) -> dict[str, Any]:
    """创建模拟支付订单（测试用）"""
    out_trade_no = generate_out_trade_no()
    time_stamp = str(int(time.time()))
    nonce_str = generate_nonce_str()
    
    # 模拟的支付参数
    pay_params = {
        "timeStamp": time_stamp,
        "nonceStr": nonce_str,
        "package": f"prepay_id=mock_{out_trade_no}",
        "signType": "MD5",
        "paySign": "MOCK_SIGN_FOR_TEST",
    }
    
    return {
        "code": 0,
        "data": {
            "out_trade_no": out_trade_no,
            "pay_params": pay_params,
            "total_fee": order_data.get("total_price", 0),
            "mock": True,  # 标记为模拟支付
        },
        "msg": "支付订单创建成功（演示模式）"
    }
