#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 API 中文提交
"""

import requests
import json

# API 地址
API_BASE = 'http://127.0.0.1:5000'

def test_submit():
    """测试提交中文数据"""
    url = f'{API_BASE}/api/demand/submit'
    
    data = {
        "title": "Python中文测试标题",
        "functionalAppeal": "这是Python发送的功能诉求",
        "targetAudience": "Python目标人群",
        "budgetRange": "100000-200000",
        "expectedDeliveryTime": "2024-12-31",
        "submitterId": "USER_PYTHON_TEST",
        "submitterName": "Python测试用户",
        "submitterPhone": "13800138000"
    }
    
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    print("提交数据:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print()
    
    response = requests.post(url, json=data, headers=headers)
    print(f"响应状态: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    return response.json()

def test_query(submitter_id):
    """测试查询数据"""
    url = f'{API_BASE}/api/demand/list?submitterId={submitter_id}&page=1&pageSize=10'
    
    response = requests.get(url)
    result = response.json()
    
    if result.get('code') == 200:
        items = result['data']['list']
        print("\n查询结果:")
        for item in items:
            print(f"  标题: {item.get('title')}")
            print(f"  目标人群: {item.get('targetAudience')}")
            print(f"  提交人: {item.get('submitterName')}")
            print()

if __name__ == '__main__':
    print("=" * 60)
    print("测试 API 中文提交")
    print("=" * 60)
    
    # 提交数据
    result = test_submit()
    
    # 查询数据
    if result.get('code') == 200:
        test_query("USER_PYTHON_TEST")
