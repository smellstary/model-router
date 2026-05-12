App({
  globalData: {
    userInfo: null,
    region: null,
    weather: null,
    plots: []
  },

  onLaunch() {
    this.initStorage();
    this.checkUserRegion();
  },

  initStorage() {
    const safeSet = require('./utils/storage.js').safeSet;
    const safeGet = require('./utils/storage.js').safeGet;

    if (!safeGet('firstLaunch')) {
      safeSet('firstLaunch', true);
      safeSet('reminders', []);
      safeSet('diaries', []);
      safeSet('customCrops', []);
    }
  },

  checkUserRegion() {
    const safeGet = require('./utils/storage.js').safeGet;
    const region = safeGet('userRegion');

    if (!region) {
      wx.navigateTo({
        url: '/pages/region/region'
      });
    } else {
      this.globalData.region = region;
    }
  },

  setUserRegion(region) {
    const safeSet = require('./utils/storage.js').safeSet;
    safeSet('userRegion', region);
    this.globalData.region = region;
  },

  request(url, data = {}, method = 'GET') {
    return new Promise((resolve, reject) => {
      wx.request({
        url: url,
        data: data,
        method: method,
        header: {
          'content-type': 'application/json'
        },
        timeout: 10000,
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(res);
          }
        },
        fail: (err) => {
          reject(err);
        }
      });
    });
  },

  getWeather(latitude, longitude) {
    const weather = require('./utils/weather.js');
    return weather.getWeather(latitude, longitude);
  }
})
