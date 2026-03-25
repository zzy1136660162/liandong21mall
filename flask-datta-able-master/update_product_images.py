from apps import db
from apps import create_app
from apps.config import config_dict

app = create_app(config_dict['Debug'])
app.app_context().push()

from apps.sp_mall.sp_models import SpProduct

products = SpProduct.query.filter(SpProduct.images.is_(None)).all()
print(f'需要更新图片的商品数量: {len(products)}')

for p in products:
    p.images = [p.main_image]
    print(f'  - 更新商品 {p.id}: {p.product_name}')

db.session.commit()
print('更新完成')
