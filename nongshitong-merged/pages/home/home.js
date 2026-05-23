const app = getApp();
const solarTerms = require('../../utils/solarTerms.js');
const plots = require('../../utils/plots.js');
const reminder = require('../../utils/reminder.js');
const weather = require('../../utils/weather.js');

Page({
  data: {
    currentDate: '',
    lunarDate: '',
    location: '定位中...',
    currentSolarTerm: {},
    nextSolarTerm: {},
    daysToNextTerm: 0,
    temperature: '--',
    humidity: '--',
    weather: '暂无数据',
    windSpeed: '--',
    weatherIcon: '🌤️',
    weatherTips: ['天气数据加载中...'],
    todayReminders: [],
    isLoading: true
  },

  onLoad() {
    this.initHomePage();
  },

  onShow() {
    this.loadReminders();
  },

  onPullDownRefresh() {
    this.initHomePage();
    setTimeout(() => {
      wx.stopPullDownRefresh();
    }, 1000);
  },

  initHomePage() {
    this.setDateInfo();
    this.setSolarTermInfo();
    this.loadLocation();
    this.loadWeather();
    this.loadReminders();
  },

  setDateInfo() {
    const now = new Date();
    const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    const dateStr = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`;
    const weekDay = weekDays[now.getDay()];
    this.setData({
      currentDate: `${weekDay} ${dateStr}`,
      lunarDate: '农历信息加载中...'
    });
  },

  setSolarTermInfo() {
    const { currentTerm, nextTerm } = solarTerms.getCurrentSolarTerm();
    if (currentTerm) {
      const now = new Date();
      let nextTermDate = new Date(now.getFullYear(), nextTerm.month - 1, nextTerm.day);
      if (nextTermDate < now) {
        nextTermDate = new Date(now.getFullYear() + 1, nextTerm.month - 1, nextTerm.day);
      }
      const daysToNext = Math.ceil((nextTermDate - now) / (1000 * 60 * 60 * 24));

      this.setData({
        currentSolarTerm: currentTerm,
        nextSolarTerm: nextTerm,
        daysToNextTerm: daysToNext
      });
    }
  },

  loadLocation() {
    const storage = require('../../utils/storage.js');
    const region = storage.safeGet('userRegion');
    if (region) {
      this.setData({
        location: region
      });
    } else {
      this.setData({
        location: '未设置地区'
      });
    }
  },

  async loadWeather() {
    try {
      const res = await new Promise((resolve, reject) => {
        wx.getLocation({
          type: 'gcj02',
          success: resolve,
          fail: reject
        });
      });

      const weatherData = await weather.getWeather(res.latitude, res.longitude);
      const tips = weather.getWeatherAdvice(weatherData.temperature, weatherData.weather);

      this.setData({
        temperature: weatherData.temperature,
        humidity: weatherData.humidity,
        weather: weatherData.weather,
        windSpeed: weatherData.windSpeed,
        weatherIcon: weather.getWeatherIcon(weatherData.weather),
        weatherTips: tips,
        isLoading: false
      });
    } catch (error) {
      console.log('Weather load error:', error);
      this.setData({
        weatherTips: ['定位失败，使用默认天气'],
        isLoading: false
      });
    }
  },

  loadReminders() {
    const plotsData = plots.loadPlots();
    const storage = require('../../utils/storage.js');
    const region = storage.safeGet('userRegion');
    const reminders = reminder.generateReminders(plotsData, region);
    const today = this.formatDate(new Date());

    const todayReminders = reminders.filter(r => r.date === today).slice(0, 5);

    const savedReminders = reminder.loadReminders();
    const mergedReminders = todayReminders.map(tr => {
      const saved = savedReminders.find(sr => sr.id === tr.id);
      return saved ? { ...tr, ...saved } : tr;
    });

    this.setData({
      todayReminders: mergedReminders
    });
  },

  formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  },

  onLocationTap() {
    wx.navigateTo({
      url: '/pages/region/region'
    });
  },

  goToReminder() {
    wx.switchTab({
      url: '/pages/reminder/reminder'
    });
  },

  goToAddPlot() {
    wx.navigateTo({
      url: '/pages/my-field/my-field'
    });
  },

  goToCrops() {
    wx.switchTab({
      url: '/pages/crops/crops'
    });
  },

  goToEncyclopedia() {
    wx.navigateTo({
      url: '/pages/encyclopedia/encyclopedia'
    });
  },

  goToTimeline() {
    wx.switchTab({
      url: '/pages/timeline/timeline'
    });
  }
});
