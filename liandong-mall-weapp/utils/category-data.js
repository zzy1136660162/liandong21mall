// 分类数据配置
const categories = [
  {
    id: 'all',
    name: '全部',
    icon: '',
    subCategories: []
  },
  {
    id: 'food',
    name: '零食饮料',
    icon: 'https://picsum.photos/80/80?random=100',
    subCategories: [
      { id: 'recommend', name: '好物推荐', icon: 'https://picsum.photos/80/80?random=101' },
      { id: 'official', name: '官方精选', icon: 'https://picsum.photos/80/80?random=102' },
      { id: 'drink', name: '冲调饮品', icon: 'https://picsum.photos/80/80?random=103' },
      { id: 'nuts', name: '坚果炒货', icon: 'https://picsum.photos/80/80?random=104' },
      { id: 'instant', name: '方便速食', icon: 'https://picsum.photos/80/80?random=105' },
      { id: 'candy', name: '糖巧蜜饯', icon: 'https://picsum.photos/80/80?random=106' },
      { id: 'dried', name: '豆干肉干', icon: 'https://picsum.photos/80/80?random=107' },
      { id: 'bakery', name: '面包糕点', icon: 'https://picsum.photos/80/80?random=108' },
      { id: 'beverage', name: '饮料', icon: 'https://picsum.photos/80/80?random=109' },
      { id: 'chips', name: '饼干膨化', icon: 'https://picsum.photos/80/80?random=110' }
    ]
  },
  {
    id: 'home',
    name: '家居百货',
    icon: 'https://picsum.photos/80/80?random=200',
    subCategories: [
      { id: 'furniture', name: '家具', icon: 'https://picsum.photos/80/80?random=201' },
      { id: 'textile', name: '家居家纺', icon: 'https://picsum.photos/80/80?random=202' },
      { id: 'cleaning', name: '家用清洁', icon: 'https://picsum.photos/80/80?random=203' },
      { id: 'bedding', name: '床上用品', icon: 'https://picsum.photos/80/80?random=204' },
      { id: 'daily', name: '生活日用', icon: 'https://picsum.photos/80/80?random=205' },
      { id: 'tissue', name: '纸品湿巾', icon: 'https://picsum.photos/80/80?random=206' },
      { id: 'festival', name: '节日婚庆', icon: 'https://picsum.photos/80/80?random=207' },
      { id: 'pet', name: '花宠用品', icon: 'https://picsum.photos/80/80?random=208' },
      { id: 'car', name: '车品工业品', icon: 'https://picsum.photos/80/80?random=209' },
      { id: 'kitchen', name: '餐厨用具', icon: 'https://picsum.photos/80/80?random=210' }
    ]
  },
  {
    id: 'clothing',
    name: '女装女鞋',
    icon: 'https://picsum.photos/80/80?random=300',
    subCategories: [
      { id: 'tops', name: '上装', icon: 'https://picsum.photos/80/80?random=301' },
      { id: 'underwear', name: '内衣裤袜', icon: 'https://picsum.photos/80/80?random=302' },
      { id: 'outerwear', name: '外套', icon: 'https://picsum.photos/80/80?random=303' },
      { id: 'suit', name: '套装', icon: 'https://picsum.photos/80/80?random=304' },
      { id: 'bags', name: '女士包袋', icon: 'https://picsum.photos/80/80?random=305' },
      { id: 'shoes', name: '女鞋', icon: 'https://picsum.photos/80/80?random=306' },
      { id: 'homewear', name: '家居服', icon: 'https://picsum.photos/80/80?random=307' },
      { id: 'accessories', name: '服装配饰', icon: 'https://picsum.photos/80/80?random=308' },
      { id: 'dress', name: '裙装', icon: 'https://picsum.photos/80/80?random=309' },
      { id: 'pants', name: '裤装', icon: 'https://picsum.photos/80/80?random=310' }
    ]
  },
  {
    id: 'beauty',
    name: '美妆护肤',
    icon: 'https://picsum.photos/80/80?random=400',
    subCategories: [
      { id: 'recommend', name: '好物推荐', icon: 'https://picsum.photos/80/80?random=401' },
      { id: 'official', name: '官方精选', icon: 'https://picsum.photos/80/80?random=402' },
      { id: 'makeup', name: '女士彩妆', icon: 'https://picsum.photos/80/80?random=403' },
      { id: 'skincare', name: '女士护肤', icon: 'https://picsum.photos/80/80?random=404' },
      { id: 'men-makeup', name: '男士彩妆', icon: 'https://picsum.photos/80/80?random=405' },
      { id: 'men-skincare', name: '男士护肤', icon: 'https://picsum.photos/80/80?random=406' },
      { id: 'hair', name: '美发用品', icon: 'https://picsum.photos/80/80?random=407' },
      { id: 'tools', name: '美妆工具', icon: 'https://picsum.photos/80/80?random=408' },
      { id: 'perfume', name: '美妆香水', icon: 'https://picsum.photos/80/80?random=409' },
      { id: 'sunscreen', name: '防晒护理', icon: 'https://picsum.photos/80/80?random=410' }
    ]
  },
  {
    id: 'personal',
    name: '个护清洁',
    icon: 'https://picsum.photos/80/80?random=500',
    subCategories: [
      { id: 'instrument', name: '个护仪器', icon: 'https://picsum.photos/80/80?random=501' },
      { id: 'oral', name: '口腔护理', icon: 'https://picsum.photos/80/80?random=502' },
      { id: 'feminine', name: '女性护理', icon: 'https://picsum.photos/80/80?random=503' },
      { id: 'haircare', name: '洗发护发', icon: 'https://picsum.photos/80/80?random=504' },
      { id: 'body', name: '身体护理', icon: 'https://picsum.photos/80/80?random=505' }
    ]
  },
  {
    id: 'health',
    name: '医疗保健',
    icon: 'https://picsum.photos/80/80?random=600',
    subCategories: [
      { id: 'recommend', name: '好物推荐', icon: 'https://picsum.photos/80/80?random=601' },
      { id: 'official', name: '官方精选', icon: 'https://picsum.photos/80/80?random=602' },
      { id: 'tonic', name: '传统滋补', icon: 'https://picsum.photos/80/80?random=603' },
      { id: 'medical', name: '医用器械', icon: 'https://picsum.photos/80/80?random=604' },
      { id: 'nutrition', name: '营养保健', icon: 'https://picsum.photos/80/80?random=605' }
    ]
  },
  {
    id: 'baby',
    name: '母婴玩具',
    icon: 'https://picsum.photos/80/80?random=700',
    subCategories: [
      { id: 'recommend', name: '好物推荐', icon: 'https://picsum.photos/80/80?random=701' },
      { id: 'kids', name: '儿童用品', icon: 'https://picsum.photos/80/80?random=702' },
      { id: 'books', name: '图书文娱', icon: 'https://picsum.photos/80/80?random=703' },
      { id: 'milk', name: '奶粉辅食', icon: 'https://picsum.photos/80/80?random=704' },
      { id: 'baby-products', name: '婴儿用品', icon: 'https://picsum.photos/80/80?random=705' },
      { id: 'baby-clothes', name: '婴童服饰', icon: 'https://picsum.photos/80/80?random=706' },
      { id: 'maternity', name: '孕妇专用', icon: 'https://picsum.photos/80/80?random=707' },
      { id: 'kids-shoes', name: '时尚童鞋', icon: 'https://picsum.photos/80/80?random=708' },
      { id: 'trendy-kids', name: '潮流童装', icon: 'https://picsum.photos/80/80?random=709' },
      { id: 'toys', name: '玩具学习', icon: 'https://picsum.photos/80/80?random=710' }
    ]
  },
  {
    id: 'fresh',
    name: '生鲜食品',
    icon: 'https://picsum.photos/80/80?random=800',
    subCategories: [
      { id: 'recommend', name: '好物推荐', icon: 'https://picsum.photos/80/80?random=801' },
      { id: 'frozen', name: '冷冻食品', icon: 'https://picsum.photos/80/80?random=802' },
      { id: 'fruit', name: '水果', icon: 'https://picsum.photos/80/80?random=803' },
      { id: 'seafood', name: '海鲜水产', icon: 'https://picsum.photos/80/80?random=804' },
      { id: 'baking', name: '烘焙原料', icon: 'https://picsum.photos/80/80?random=805' },
      { id: 'meat', name: '猪牛羊肉', icon: 'https://picsum.photos/80/80?random=806' },
      { id: 'poultry', name: '禽类肉制品', icon: 'https://picsum.photos/80/80?random=807' },
      { id: 'oil', name: '粮油调味', icon: 'https://picsum.photos/80/80?random=808' },
      { id: 'vegetable', name: '蔬菜', icon: 'https://picsum.photos/80/80?random=809' },
      { id: 'egg', name: '蛋类', icon: 'https://picsum.photos/80/80?random=810' }
    ]
  },
  {
    id: 'men',
    name: '男装男鞋',
    icon: 'https://picsum.photos/80/80?random=900',
    subCategories: [
      { id: 'recommend', name: '好物推荐', icon: 'https://picsum.photos/80/80?random=901' },
      { id: 'official', name: '官方精选', icon: 'https://picsum.photos/80/80?random=902' },
      { id: 'tops', name: '上装', icon: 'https://picsum.photos/80/80?random=903' },
      { id: 'underwear', name: '内裤', icon: 'https://picsum.photos/80/80?random=904' },
      { id: 'outerwear', name: '外套', icon: 'https://picsum.photos/80/80?random=905' },
      { id: 'suit', name: '套装', icon: 'https://picsum.photos/80/80?random=906' },
      { id: 'accessories', name: '服饰配饰', icon: 'https://picsum.photos/80/80?random=907' },
      { id: 'bags', name: '男士包袋', icon: 'https://picsum.photos/80/80?random=908' },
      { id: 'shoes', name: '男鞋', icon: 'https://picsum.photos/80/80?random=909' },
      { id: 'pants', name: '裤装', icon: 'https://picsum.photos/80/80?random=910' }
    ]
  },
  {
    id: 'sports',
    name: '运动户外',
    icon: 'https://picsum.photos/80/80?random=1000',
    subCategories: [
      { id: 'official', name: '官方精选', icon: 'https://picsum.photos/80/80?random=1001' },
      { id: 'sports-goods', name: '体育用品', icon: 'https://picsum.photos/80/80?random=1002' },
      { id: 'outdoor', name: '户外装备', icon: 'https://picsum.photos/80/80?random=1003' },
      { id: 'sportswear', name: '运动服', icon: 'https://picsum.photos/80/80?random=1004' },
      { id: 'sports-shoes', name: '运动鞋', icon: 'https://picsum.photos/80/80?random=1005' }
    ]
  },
  {
    id: 'digital',
    name: '数码家电',
    icon: 'https://picsum.photos/80/80?random=1100',
    subCategories: [
      { id: '3c', name: '3c电子', icon: 'https://picsum.photos/80/80?random=1101' },
      { id: 'secondhand', name: '二手电子', icon: 'https://picsum.photos/80/80?random=1102' },
      { id: 'appliance', name: '家用电器', icon: 'https://picsum.photos/80/80?random=1103' },
      { id: 'mobile', name: '手机数码', icon: 'https://picsum.photos/80/80?random=1104' },
      { id: 'accessories', name: '电子配件', icon: 'https://picsum.photos/80/80?random=1105' }
    ]
  },
  {
    id: 'luxury',
    name: '珠宝奢品',
    icon: 'https://picsum.photos/80/80?random=1200',
    subCategories: [
      { id: 'recommend', name: '好物推荐', icon: 'https://picsum.photos/80/80?random=1201' },
      { id: 'watch', name: '手表', icon: 'https://picsum.photos/80/80?random=1202' },
      { id: 'fashion', name: '时尚饰品', icon: 'https://picsum.photos/80/80?random=1203' },
      { id: 'jade', name: '玉石收藏', icon: 'https://picsum.photos/80/80?random=1204' },
      { id: 'jewelry', name: '金银首饰', icon: 'https://picsum.photos/80/80?random=1205' }
    ]
  },
  {
    id: 'tea',
    name: '茶叶酒水',
    icon: 'https://picsum.photos/80/80?random=1300',
    subCategories: [
      { id: 'recommend', name: '好物推荐', icon: 'https://picsum.photos/80/80?random=1301' },
      { id: 'official', name: '官方精选', icon: 'https://picsum.photos/80/80?random=1302' },
      { id: 'teaware', name: '茶具', icon: 'https://picsum.photos/80/80?random=1303' },
      { id: 'tea', name: '茶叶', icon: 'https://picsum.photos/80/80?random=1304' },
      { id: 'alcohol', name: '酒类', icon: 'https://picsum.photos/80/80?random=1305' }
    ]
  }
];

// 筛选标签
const filterTags = [
  { id: 'kuaishou', name: '快手优选' },
  { id: 'hot', name: '爆品计划' },
  { id: 'nationwide', name: '全国可售' },
  { id: 'sample-back', name: '买样后返' }
];

module.exports = {
  categories,
  filterTags
};
