/**
 * 分类数据
 */

const categories = [
  {
    id: 'food',
    name: '食品生鲜',
    icon: '🍔',
    subCategories: [
      { id: 'snacks', name: '休闲零食' },
      { id: 'drinks', name: '饮料冲调' },
      { id: 'fresh', name: '生鲜果蔬' },
      { id: 'grains', name: '粮油调味' },
      { id: 'tea', name: '茗茶' },
      { id: 'wine', name: '酒类' }
    ]
  },
  {
    id: 'home',
    name: '家居日用',
    icon: '🏠',
    subCategories: [
      { id: 'cleaning', name: '清洁用品' },
      { id: 'kitchen', name: '厨房用具' },
      { id: 'storage', name: '收纳整理' },
      { id: 'textile', name: '家纺布艺' },
      { id: 'decor', name: '家居装饰' }
    ]
  },
  {
    id: 'clothing',
    name: '服饰内衣',
    icon: '👔',
    subCategories: [
      { id: 'women', name: '女装' },
      { id: 'men', name: '男装' },
      { id: 'underwear', name: '内衣' },
      { id: 'shoes', name: '鞋靴' },
      { id: 'bags', name: '箱包' },
      { id: 'accessories', name: '配饰' }
    ]
  },
  {
    id: 'beauty',
    name: '美妆护肤',
    icon: '💄',
    subCategories: [
      { id: 'skincare', name: '面部护肤' },
      { id: 'makeup', name: '彩妆' },
      { id: 'perfume', name: '香氛' },
      { id: 'tools', name: '美妆工具' },
      { id: 'beauty-devices', name: '美容仪器' }
    ]
  },
  {
    id: 'personal',
    name: '个护清洁',
    icon: '🧴',
    subCategories: [
      { id: 'hair', name: '洗发护发' },
      { id: 'body', name: '身体护理' },
      { id: 'oral', name: '口腔护理' },
      { id: 'feminine', name: '女性护理' }
    ]
  },
  {
    id: 'digital',
    name: '数码家电',
    icon: '📱',
    subCategories: [
      { id: 'phones', name: '手机通讯' },
      { id: 'computers', name: '电脑办公' },
      { id: 'appliances', name: '家用电器' },
      { id: 'smart', name: '智能设备' },
      { id: 'accessories-digital', name: '数码配件' }
    ]
  },
  {
    id: 'sports',
    name: '运动户外',
    icon: '⚽',
    subCategories: [
      { id: 'fitness', name: '运动健身' },
      { id: 'outdoor', name: '户外装备' },
      { id: 'sports-shoes', name: '运动鞋包' },
      { id: 'cycling', name: '骑行运动' }
    ]
  },
  {
    id: 'toys',
    name: '母婴玩具',
    icon: '🍼',
    subCategories: [
      { id: 'baby-food', name: '奶粉辅食' },
      { id: 'diapers', name: '尿裤湿巾' },
      { id: 'baby-care', name: '洗护用品' },
      { id: 'toys-games', name: '玩具乐器' },
      { id: 'baby-gear', name: '孕产用品' }
    ]
  }
];

module.exports = {
  categories
};
