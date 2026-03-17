-- 会员达人模块演示数据
-- 用于测试和演示

-- =====================================================
-- 1. 插入演示用户
-- =====================================================
INSERT INTO `user` (`id`, `openid`, `unionid`, `nickname`, `avatar`, `phone`, `status`, `created_at`) VALUES
(1, 'test_openid_001', NULL, '测试用户1', 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png', '13800138001', 1, '2024-01-01 10:00:00'),
(2, 'test_openid_002', NULL, '测试用户2', 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png', '13800138002', 1, '2024-01-02 10:00:00'),
(3, 'test_openid_003', NULL, 'VIP用户1', 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png', '13800138003', 1, '2024-01-03 10:00:00'),
(4, 'test_openid_004', NULL, '达人用户1', 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png', '13800138004', 1, '2024-01-04 10:00:00'),
(5, 'test_openid_005', NULL, '待审核达人', 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png', '13800138005', 1, '2024-01-05 10:00:00');

-- =====================================================
-- 2. 插入用户会员关系
-- =====================================================
-- 普通用户（无会员记录）

-- VIP用户（用户3）
INSERT INTO `user_member` (`id`, `user_id`, `level_id`, `level_code`, `upgrade_type`, `upgrade_time`, `first_order_id`, `valid_start`, `valid_end`, `created_at`) VALUES
(1, 3, 2, 'vip', 1, '2024-01-05 15:30:00', 1001, '2024-01-05 15:30:00', NULL, '2024-01-05 15:30:00');

-- 达人用户（用户4）- 也是VIP
INSERT INTO `user_member` (`id`, `user_id`, `level_id`, `level_code`, `upgrade_type`, `upgrade_time`, `first_order_id`, `valid_start`, `valid_end`, `created_at`) VALUES
(2, 4, 2, 'vip', 1, '2024-01-06 10:00:00', 1002, '2024-01-06 10:00:00', NULL, '2024-01-06 10:00:00');

-- 待审核达人（用户5）- 也是VIP
INSERT INTO `user_member` (`id`, `user_id`, `level_id`, `level_code`, `upgrade_type`, `upgrade_time`, `first_order_id`, `valid_start`, `valid_end`, `created_at`) VALUES
(3, 5, 2, 'vip', 1, '2024-01-07 10:00:00', 1003, '2024-01-07 10:00:00', NULL, '2024-01-07 10:00:00');

-- =====================================================
-- 3. 插入达人申请记录
-- =====================================================
-- 用户2：未申请（无记录）

-- 用户3：已拒绝
INSERT INTO `talent_apply` (`id`, `user_id`, `real_name`, `phone`, `region`, `apply_reason`, `intro`, `status`, `reject_reason`, `audit_time`, `audit_by`, `created_at`) VALUES
(1, 3, 'VIP用户1', '13800138003', '广东省深圳市', '希望成为达人进行推广', '有丰富的电商经验', 'REJECTED', '申请信息不完整，请补充更多推广资源说明', '2024-01-06 14:00:00', 1, '2024-01-06 10:00:00');

-- 用户4：已通过
INSERT INTO `talent_apply` (`id`, `user_id`, `real_name`, `phone`, `region`, `apply_reason`, `intro`, `status`, `reject_reason`, `audit_time`, `audit_by`, `created_at`) VALUES
(2, 4, '达人用户1', '13800138004', '湖北省武汉市', '有10万私域粉丝，希望推广平台商品', '从事电商推广5年，年GMV 500万+', 'APPROVED', NULL, '2024-01-07 10:00:00', 1, '2024-01-07 09:00:00');

-- 用户5：审核中
INSERT INTO `talent_apply` (`id`, `user_id`, `real_name`, `phone`, `region`, `apply_reason`, `intro`, `status`, `reject_reason`, `audit_time`, `audit_by`, `created_at`) VALUES
(3, 5, '待审核达人', '13800138005', '浙江省杭州市', '有社群运营经验，想成为达人', '微商转型，有5000+微信好友', 'PENDING', NULL, NULL, NULL, '2024-01-08 10:00:00');

-- =====================================================
-- 4. 插入用户地址
-- =====================================================
INSERT INTO `user_address` (`id`, `user_id`, `name`, `phone`, `province`, `city`, `district`, `detail`, `is_default`, `created_at`) VALUES
(1, 1, '张三', '13800138001', '广东省', '广州市', '天河区', '天河路123号', 1, '2024-01-01 11:00:00'),
(2, 3, 'VIP用户', '13800138003', '广东省', '深圳市', '南山区', '科技园南路456号', 1, '2024-01-05 16:00:00'),
(3, 4, '达人用户', '13800138004', '湖北省', '武汉市', '洪山区', '珞瑜路789号', 1, '2024-01-06 11:00:00');

-- =====================================================
-- 演示数据说明
-- =====================================================
-- 
-- 用户1: 测试用户1 - 普通用户，无会员，无达人申请
-- 用户2: 测试用户2 - 普通用户，无会员，无达人申请  
-- 用户3: VIP用户1 - VIP会员，已被拒绝达人申请
-- 用户4: 达人用户1 - VIP会员，已通过达人申请（可进入达人中心）
-- 用户5: 待审核达人 - VIP会员，达人申请审核中
--
-- 测试API时可通过设置请求头 X-User-Id 来切换用户
-- 例如：X-User-Id: 1 返回用户1的信息
--
