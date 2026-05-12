const storage = require('../../utils/storage.js');
const weather = require('../../utils/weather.js');

const PROVINCES = [
  '北京市', '天津市', '上海市', '重庆市',
  '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省',
  '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省',
  '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '台湾省',
  '内蒙古自治区', '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区',
  '香港特别行政区', '澳门特别行政区'
];

Page({
  data: {
    regions: PROVINCES,
    filteredRegions: PROVINCES,
    searchKey: '',
    selectedRegion: ''
  },

  onLoad() {
    const savedRegion = storage.safeGet('userRegion');
    if (savedRegion) {
      this.setData({ selectedRegion: savedRegion });
    }
  },

  onSearch(e) {
    const key = e.detail.value;
    this.setData({ searchKey: key });

    if (key) {
      const filtered = PROVINCES.filter(r => r.includes(key));
      this.setData({ filteredRegions: filtered });
    } else {
      this.setData({ filteredRegions: PROVINCES });
    }
  },

  selectRegion(e) {
    const region = e.currentTarget.dataset.region;
    this.setData({ selectedRegion: region });

    const app = getApp();
    app.setUserRegion(region);

    wx.showToast({
      title: '设置成功',
      icon: 'success'
    });

    setTimeout(() => {
      wx.navigateBack();
    }, 1500);
  },

  getLocation() {
    wx.getLocation({
      type: 'gcj02',
      success: (res) => {
        wx.showToast({
          title: '定位成功',
          icon: 'success'
        });
      },
      fail: () => {
        wx.showToast({
          title: '定位失败',
          icon: 'none'
        });
      }
    });
  }
});
