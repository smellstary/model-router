const CROPS = [
  {
    id: 'rice',
    name: '水稻',
    icon: '🌾',
    category: '粮食作物',
    growthPeriod: '120-150天',
    suitableTemperature: '20-35℃',
    suitableSoil: '壤土、黏土',
    suitableRegion: '南方水田区',
    stages: [
      { name: '播种', solarTerm: '清明', description: '浸种催芽，适时播种' },
      { name: '育秧', solarTerm: '谷雨', description: '苗床管理，炼苗蹲苗' },
      { name: '插秧', solarTerm: '立夏', description: '适时移栽，合理密植' },
      { name: '分蘖', solarTerm: '小满', description: '浅水灌溉，早施分蘖肥' },
      { name: '拔节', solarTerm: '夏至', description: '排水晒田，控制无效分蘖' },
      { name: '抽穗', solarTerm: '大暑', description: '深水护胎，巧施穗肥' },
      { name: '成熟', solarTerm: '秋分', description: '适时收割，干燥入仓' }
    ],
    tips: ['喜温喜湿', '需充足水分', '忌连作']
  },
  {
    id: 'wheat',
    name: '小麦',
    icon: '🌾',
    category: '粮食作物',
    growthPeriod: '220-270天',
    suitableTemperature: '12-25℃',
    suitableSoil: '壤土、沙壤土',
    suitableRegion: '北方旱作区',
    stages: [
      { name: '播种', solarTerm: '秋分', description: '适期播种，深度3-5厘米' },
      { name: '出苗', solarTerm: '寒露', description: '查苗补苗，确保全苗' },
      { name: '分蘖', solarTerm: '霜降', description: '中耕松土，促进分蘖' },
      { name: '越冬', solarTerm: '小雪', description: '浇越冬水，保暖防寒' },
      { name: '返青', solarTerm: '雨水', description: '早春管理，追返青肥' },
      { name: '拔节', solarTerm: '春分', description: '重施拔节肥，防倒伏' },
      { name: '成熟', solarTerm: '小满', description: '适时收割，晾晒入仓' }
    ],
    tips: ['耐寒性强', '需春化作用', '忌湿涝']
  },
  {
    id: 'corn',
    name: '玉米',
    icon: '🌽',
    category: '粮食作物',
    growthPeriod: '100-130天',
    suitableTemperature: '18-35℃',
    suitableSoil: '壤土、砂壤土',
    suitableRegion: '全国各地区',
    stages: [
      { name: '播种', solarTerm: '立夏', description: '地温稳定通过15℃播种' },
      { name: '出苗', solarTerm: '小满', description: '查苗补苗，中耕除草' },
      { name: '拔节', solarTerm: '芒种', description: '轻施苗肥，深中耕' },
      { name: '抽雄', solarTerm: '小暑', description: '重施穗肥，培土防倒' },
      { name: '吐丝', solarTerm: '大暑', description: '人工授粉，去除分蘖' },
      { name: '成熟', solarTerm: '处暑', description: '适时晚收，提高产量' }
    ],
    tips: ['喜温耐旱', '需大肥大水', '喜光照']
  },
  {
    id: 'soybean',
    name: '大豆',
    icon: '🫘',
    category: '油料作物',
    growthPeriod: '100-120天',
    suitableTemperature: '15-30℃',
    suitableSoil: '壤土、砂壤土',
    suitableRegion: '东北、黄淮地区',
    stages: [
      { name: '播种', solarTerm: '立夏', description: '适温播种，深度3-4厘米' },
      { name: '出苗', solarTerm: '小满', description: '查苗补种，中耕除草' },
      { name: '分枝', solarTerm: '夏至', description: '及时中耕，防治病虫害' },
      { name: '开花', solarTerm: '小暑', description: '叶面施肥，保湿防旱' },
      { name: '结荚', solarTerm: '大暑', description: '防治虫害，增施磷钾' },
      { name: '成熟', solarTerm: '白露', description: '适时收割，及时晾晒' }
    ],
    tips: ['固氮作物', '忌连作', '需磷钾肥']
  },
  {
    id: 'cotton',
    name: '棉花',
    icon: '🌸',
    category: '经济作物',
    growthPeriod: '150-180天',
    suitableTemperature: '20-30℃',
    suitableSoil: '壤土、黏土',
    suitableRegion: '新疆、黄河流域',
    stages: [
      { name: '播种', solarTerm: '谷雨', description: '地温稳定通过15℃播种' },
      { name: '出苗', solarTerm: '小满', description: '查苗补苗，间苗定苗' },
      { name: '现蕾', solarTerm: '夏至', description: '中耕培土，追蕾肥' },
      { name: '开花', solarTerm: '小暑', description: '整枝打杈，防治病虫' },
      { name: '结铃', solarTerm: '大暑', description: '重施花铃肥，保湿防旱' },
      { name: '吐絮', solarTerm: '白露', description: '适时采摘，分级存放' }
    ],
    tips: ['喜温好光', '耐旱怕涝', '需整枝']
  },
  {
    id: 'vegetable',
    name: '蔬菜',
    icon: '🥬',
    category: '蔬菜作物',
    growthPeriod: '60-90天',
    suitableTemperature: '15-28℃',
    suitableSoil: '疏松肥沃土',
    suitableRegion: '全国各地区',
    stages: [
      { name: '整地', solarTerm: '惊蛰', description: '深翻土壤，施足基肥' },
      { name: '播种', solarTerm: '春分', description: '根据品种适时播种' },
      { name: '出苗', solarTerm: '清明', description: '保持土壤湿润' },
      { name: '定植', solarTerm: '谷雨', description: '选壮苗适时定植' },
      { name: '生长', solarTerm: '立夏', description: '加强肥水管理' },
      { name: '采收', solarTerm: '小满', description: '适时采收，保鲜上市' }
    ],
    tips: ['种类繁多', '周期短', '效益高']
  },
  {
    id: 'fruit',
    name: '水果',
    icon: '🍎',
    category: '果树作物',
    growthPeriod: '180-365天',
    suitableTemperature: '15-28℃',
    suitableSoil: '壤土、砂壤土',
    suitableRegion: '全国各地区',
    stages: [
      { name: '修剪', solarTerm: '小寒', description: '冬季修剪，调整树形' },
      { name: '萌芽', solarTerm: '惊蛰', description: '追施萌芽肥' },
      { name: '开花', solarTerm: '清明', description: '花期管理，辅助授粉' },
      { name: '结果', solarTerm: '小满', description: '疏花疏果，防治病虫害' },
      { name: '膨大', solarTerm: '夏至', description: '追施膨果肥，套袋保护' },
      { name: '成熟', solarTerm: '立秋', description: '适时采收，分级包装' }
    ],
    tips: ['品种多样', '收益高', '管理周期长']
  },
  {
    id: 'tea',
    name: '茶叶',
    icon: '🍵',
    category: '经济作物',
    growthPeriod: '常年采收',
    suitableTemperature: '15-25℃',
    suitableSoil: '酸性红黄壤',
    suitableRegion: '南方丘陵山区',
    stages: [
      { name: '修剪', solarTerm: '大寒', description: '茶园修剪，清理越冬病虫害' },
      { name: '催芽', solarTerm: '雨水', description: '浅耕松土，追施催芽肥' },
      { name: '开采', solarTerm: '惊蛰', description: '适时开采，分批采摘' },
      { name: '夏茶', solarTerm: '小满', description: '合理采摘，养采结合' },
      { name: '秋茶', solarTerm: '立秋', description: '适时停采，养树越冬' }
    ],
    tips: ['喜酸性土壤', '喜湿润', '需遮阴']
  }
];

function getAllCrops() {
  return CROPS;
}

function getCropById(id) {
  return CROPS.find(c => c.id === id);
}

function getCropByName(name) {
  return CROPS.find(c => c.name === name);
}

function getCropsByCategory(category) {
  return CROPS.filter(c => c.category === category);
}

function getCropCategories() {
  return [...new Set(CROPS.map(c => c.category))];
}

function getCropStageBySolarTerm(cropId, solarTermName) {
  const crop = getCropById(cropId);
  if (!crop) return null;
  return crop.stages.find(s => s.solarTerm === solarTermName);
}

module.exports = {
  getAllCrops,
  getCropById,
  getCropByName,
  getCropsByCategory,
  getCropCategories,
  getCropStageBySolarTerm
}
