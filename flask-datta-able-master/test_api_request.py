# -*- encoding: utf-8 -*-
"""
测试订单详情API请求
"""

import requests
import json

def test_order_detail():
    base_url = "http://localhost:5000"
    
    try:
        # 测试订单详情API
        order_id = 7
        url = f"{base_url}/api/sp/order/detail/{order_id}"
        headers = {
            "X-User-Id": "1",
            "Content-Type": "application/json"
        }
        
        print(f"请求URL: {url}")
        print(f"请求头: {headers}")
        
        response = requests.get(url, headers=headers)
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应文本: {response.text}")
        
        if response.text:
            try:
                print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
            except:
                pass
        
    except Exception as e:
        print(f"请求失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_order_detail()
