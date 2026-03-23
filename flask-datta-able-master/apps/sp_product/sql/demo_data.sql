-- 商品商城模块 - 示例数据
-- 用于测试商品列表页面功能

-- =====================================================
-- 1. 插入商品分类数据
-- =====================================================
INSERT INTO `product_category` (`parent_id`, `category_name`, `category_code`, `icon`, `sort`, `status`) VALUES
(0, '护肤', 'skincare', '/static/images/category/skincare.png', 1, 1),
(0, '彩妆', 'makeup', '/static/images/category/makeup.png', 2, 1),
(0, '个护', 'personal_care', '/static/images/category/personal_care.png', 3, 1),
(0, '食品', 'food', '/static/images/category/food.png', 4, 1),
(0, '家居', 'home', '/static/images/category/home.png', 5, 1);

-- =====================================================
-- 2. 插入商品数据
-- =====================================================
INSERT INTO `product` (`category_id`, `product_name`, `product_code`, `main_image`, `images`, `price`, `original_price`, `member_price`, `stock`, `sales`, `brief`, `description`, `status`, `is_hot`, `is_new`, `is_recommend`, `sort`) VALUES
-- 护肤类商品
(1, '温和洁面乳', 'PROD001', '/static/images/product/face_wash.jpg', '["/static/images/product/face_wash_1.jpg","/static/images/product/face_wash_2.jpg"]', 89.00, 128.00, 84.55, 100, 256, '温和清洁,不紧绷', '<p>温和洁面乳,采用天然植物精华,温和清洁肌肤,不紧绷不干燥。</p>', 1, 1, 0, 1, 10),
(1, '保湿爽肤水', 'PROD002', '/static/images/product/toner.jpg', '["/static/images/product/toner_1.jpg","/static/images/product/toner_2.jpg"]', 128.00, 168.00, 121.60, 80, 189, '深层补水,清爽不油腻', '<p>保湿爽肤水,含有透明质酸,深层补水,让肌肤水润饱满。</p>', 1, 1, 1, 1, 9),
(1, '抗皱精华液', 'PROD003', '/static/images/product/serum.jpg', '["/static/images/product/serum_1.jpg","/static/images/product/serum_2.jpg"]', 298.00, 398.00, 283.10, 50, 145, '淡化细纹,紧致肌肤', '<p>抗皱精华液,含有胜肽成分,有效淡化细纹,紧致肌肤。</p>', 1, 1, 1, 1, 8),
(1, '修护面霜', 'PROD004', '/static/images/product/cream.jpg', '["/static/images/product/cream_1.jpg","/static/images/product/cream_2.jpg"]', 198.00, 268.00, 188.10, 60, 178, '修护屏障,滋润保湿', '<p>修护面霜,含有神经酰胺,修护肌肤屏障,滋润保湿。</p>', 1, 0, 0, 1, 7),
(1, '防晒隔离乳', 'PROD005', '/static/images/product/sunscreen.jpg', '["/static/images/product/sunscreen_1.jpg","/static/images/product/sunscreen_2.jpg"]', 158.00, 198.00, 150.10, 120, 234, 'SPF50+,轻薄透气', '<p>防晒隔离乳,SPF50+,轻薄透气,有效隔离紫外线。</p>', 1, 1, 0, 0, 6),

-- 彩妆类商品
(2, '气垫BB霜', 'PROD006', '/static/images/product/bb_cream.jpg', '["/static/images/product/bb_cream_1.jpg","/static/images/product/bb_cream_2.jpg"]', 168.00, 228.00, 159.60, 90, 312, '轻薄遮瑕,自然妆感', '<p>气垫BB霜,轻薄遮瑕,自然妆感,持久不脱妆。</p>', 1, 1, 1, 1, 10),
(2, '眼线笔', 'PROD007', '/static/images/product/eyeliner.jpg', '["/static/images/product/eyeliner_1.jpg","/static/images/product/eyeliner_2.jpg"]', 68.00, 98.00, 64.60, 150, 423, '防水防晕,持久不脱色', '<p>眼线笔,防水防晕,持久不脱色,轻松画出精致眼线。</p>', 1, 0, 0, 0, 9),
(2, '口红', 'PROD008', '/static/images/product/lipstick.jpg', '["/static/images/product/lipstick_1.jpg","/static/images/product/lipstick_2.jpg"]', 188.00, 258.00, 178.60, 70, 289, '滋润不拔干,显色饱满', '<p>口红,滋润不拔干,显色饱满,打造迷人唇色。</p>', 1, 1, 1, 1, 8),
(2, '眉笔', 'PROD009', '/static/images/product/eyebrow_pencil.jpg', '["/static/images/product/eyebrow_pencil_1.jpg","/static/images/product/eyebrow_pencil_2.jpg"]', 58.00, 88.00, 55.10, 180, 356, '自然持久,不易脱色', '<p>眉笔,自然持久,不易脱色,轻松打造精致眉形。</p>', 1, 0, 0, 0, 7),
(2, '散粉', 'PROD010', '/static/images/product/loose_powder.jpg', '["/static/images/product/loose_powder_1.jpg","/static/images/product/loose_powder_2.jpg"]', 98.00, 138.00, 93.10, 100, 267, '控油定妆,轻薄透明', '<p>散粉,控油定妆,轻薄透明,打造哑光妆效。</p>', 1, 1, 0, 0, 6),

-- 个护类商品
(3, '洗发水', 'PROD011', '/static/images/product/shampoo.jpg', '["/static/images/product/shampoo_1.jpg","/static/images/product/shampoo_2.jpg"]', 78.00, 108.00, 74.10, 200, 445, '温和清洁,柔顺光泽', '<p>洗发水,温和清洁,柔顺光泽,让秀发健康亮丽。</p>', 1, 1, 0, 1, 10),
(3, '护发素', 'PROD012', '/static/images/product/conditioner.jpg', '["/static/images/product/conditioner_1.jpg","/static/images/product/conditioner_2.jpg"]', 68.00, 98.00, 64.60, 180, 378, '滋润修护,改善毛躁', '<p>护发素,滋润修护,改善毛躁,让秀发柔顺顺滑。</p>', 1, 0, 0, 0, 9),
(3, '沐浴露', 'PROD013', '/static/images/product/body_wash.jpg', '["/static/images/product/body_wash_1.jpg","/static/images/product/body_wash_2.jpg"]', 58.00, 88.00, 55.10, 220, 489, '温和清洁,滋润保湿', '<p>沐浴露,温和清洁,滋润保湿,让肌肤水润嫩滑。</p>', 1, 1, 1, 1, 8),
(3, '身体乳', 'PROD014', '/static/images/product/body_lotion.jpg', '["/static/images/product/body_lotion_1.jpg","/static/images/product/body_lotion_2.jpg"]', 88.00, 128.00, 83.60, 160, 367, '滋润保湿,嫩滑肌肤', '<p>身体乳,滋润保湿,嫩滑肌肤,让全身肌肤水润嫩滑。</p>', 1, 0, 0, 0, 7),
(3, '护手霜', 'PROD015', '/static/images/product/hand_cream.jpg', '["/static/images/product/hand_cream_1.jpg","/static/images/product/hand_cream_2.jpg"]', 38.00, 58.00, 36.10, 300, 567, '滋润修护,不油腻', '<p>护手霜,滋润修护,不油腻,让双手柔嫩细腻。</p>', 1, 1, 0, 0, 6),

-- 食品类商品
(4, '燕麦片', 'PROD016', '/static/images/product/oatmeal.jpg', '["/static/images/product/oatmeal_1.jpg","/static/images/product/oatmeal_2.jpg"]', 48.00, 68.00, 45.60, 250, 523, '营养早餐,健康美味', '<p>燕麦片,营养早餐,健康美味,富含膳食纤维。</p>', 1, 1, 1, 1, 10),
(4, '坚果礼盒', 'PROD017', '/static/images/product/nuts.jpg', '["/static/images/product/nuts_1.jpg","/static/images/product/nuts_2.jpg"]', 168.00, 228.00, 159.60, 80, 234, '精选坚果,营养美味', '<p>坚果礼盒,精选坚果,营养美味,送礼佳品。</p>', 1, 0, 0, 0, 9),
(4, '蜂蜜', 'PROD018', '/static/images/product/honey.jpg', '["/static/images/product/honey_1.jpg","/static/images/product/honey_2.jpg"]', 98.00, 138.00, 93.10, 120, 312, '天然纯正,营养丰富', '<p>蜂蜜,天然纯正,营养丰富,健康美味。</p>', 1, 1, 0, 0, 8),
(4, '茶叶礼盒', 'PROD019', '/static/images/product/tea.jpg', '["/static/images/product/tea_1.jpg","/static/images/product/tea_2.jpg"]', 288.00, 388.00, 273.60, 60, 189, '精选茶叶,清香甘醇', '<p>茶叶礼盒,精选茶叶,清香甘醇,送礼佳品。</p>', 1, 0, 0, 0, 7),
(4, '红枣', 'PROD020', '/static/images/product/red_dates.jpg', '["/static/images/product/red_dates_1.jpg","/static/images/product/red_dates_2.jpg"]', 58.00, 88.00, 55.10, 200, 423, '天然红枣,补血养颜', '<p>红枣,天然红枣,补血养颜,健康美味。</p>', 1, 1, 1, 1, 6),

-- 家居类商品
(5, '香薰蜡烛', 'PROD021', '/static/images/product/candle.jpg', '["/static/images/product/candle_1.jpg","/static/images/product/candle_2.jpg"]', 68.00, 98.00, 64.60, 150, 345, '香氛怡人,放松身心', '<p>香薰蜡烛,香氛怡人,放松身心,营造温馨氛围。</p>', 1, 1, 0, 1, 10),
(5, '收纳盒', 'PROD022', '/static/images/product/storage_box.jpg', '["/static/images/product/storage_box_1.jpg","/static/images/product/storage_box_2.jpg"]', 38.00, 58.00, 36.10, 300, 567, '简约实用,收纳整理', '<p>收纳盒,简约实用,收纳整理,让家居整洁有序。</p>', 1, 0, 0, 0, 9),
(5, '抱枕', 'PROD023', '/static/images/product/pillow.jpg', '["/static/images/product/pillow_1.jpg","/static/images/product/pillow_2.jpg"]', 88.00, 128.00, 83.60, 120, 289, '柔软舒适,装饰家居', '<p>抱枕,柔软舒适,装饰家居,提升家居品味。</p>', 1, 1, 1, 1, 8),
(5, '台灯', 'PROD024', '/static/images/product/desk_lamp.jpg', '["/static/images/product/desk_lamp_1.jpg","/static/images/product/desk_lamp_2.jpg"]', 158.00, 218.00, 150.10, 80, 234, '护眼光源,简约时尚', '<p>台灯,护眼光源,简约时尚,适合阅读学习。</p>', 1, 0, 0, 0, 7),
(5, '花瓶', 'PROD025', '/static/images/product/vase.jpg', '["/static/images/product/vase_1.jpg","/static/images/product/vase_2.jpg"]', 128.00, 188.00, 121.60, 100, 267, '简约优雅,装饰家居', '<p>花瓶,简约优雅,装饰家居,提升家居品味。</p>', 1, 1, 0, 0, 6);

-- =====================================================
-- 完成
-- =====================================================
