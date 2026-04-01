# -*- encoding: utf-8 -*-
"""
地区信息 API - 提供省市区三级联动数据
"""

import json
import os
from flask import Blueprint, send_from_directory, current_app

region_bp = Blueprint('region', __name__)

# 缓存区域数据
_region_cache = None


def get_region_data():
    """获取区域数据（带缓存）"""
    global _region_cache
    
    if _region_cache is not None:
        return _region_cache
    
    try:
        static_path = os.path.join(os.path.dirname(__file__), 'static')
        file_path = os.path.join(static_path, 'pca-code.json')
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                _region_cache = json.load(f)
                return _region_cache
    except Exception as e:
        print(f"Error loading region data: {e}")
    
    return []


@region_bp.route('/api/region/data')
def get_all_regions():
    """获取所有省市区数据"""
    data = get_region_data()
    return {
        'code': 200,
        'message': 'success',
        'data': data
    }


@region_bp.route('/api/region/provinces')
def get_provinces():
    """获取所有省份"""
    data = get_region_data()
    provinces = [{'code': p['code'], 'name': p['name']} for p in data]
    return {
        'code': 200,
        'message': 'success',
        'data': provinces
    }


@region_bp.route('/api/region/cities/<province_code>')
def get_cities(province_code):
    """根据省份编码获取城市列表"""
    data = get_region_data()
    
    for province in data:
        if province['code'] == province_code:
            cities = []
            for city in province.get('children', []):
                cities.append({
                    'code': city['code'],
                    'name': city['name']
                })
            return {
                'code': 200,
                'message': 'success',
                'data': cities
            }
    
    return {
        'code': 404,
        'message': '省份不存在',
        'data': None
    }


@region_bp.route('/api/region/districts/<province_code>/<city_code>')
def get_districts(province_code, city_code):
    """根据省份编码和城市编码获取区县列表"""
    data = get_region_data()
    
    for province in data:
        if province['code'] == province_code:
            for city in province.get('children', []):
                if city['code'] == city_code:
                    districts = []
                    for district in city.get('children', []):
                        districts.append({
                            'code': district['code'],
                            'name': district['name']
                        })
                    return {
                        'code': 200,
                        'message': 'success',
                        'data': districts
                    }
    
    return {
        'code': 404,
        'message': '城市不存在',
        'data': None
    }
