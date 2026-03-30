# -*- encoding: utf-8 -*-
"""
测试静态文件访问
"""

from apps import create_app
from apps.config import config_dict

app = create_app(config_dict['Debug'])

@app.route('/test_static')
def test_static():
    """测试静态文件"""
    return '''
    <html>
    <body>
        <h1>静态文件测试</h1>
        <img src="/static/images/products/product_1_main.jpg" alt="测试图片1">
        <br>
        <img src="/static/assets/images/logo.png" alt="测试图片2">
        <br>
        <h2>如果看到上面的图片，说明静态文件配置正常</h2>
        <h2>如果看不到图片，请检查路径</h2>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
