const plots = require('../../utils/plots.js');
const reminder = require('../../utils/reminder.js');
const storage = require('../../utils/storage.js');

Page({
  data: {
    username: '新农人',
    region: '未设置',
    avatarText: '农',
    stats: {
      plots: 0,
      crops: 0,
      reminders: 0
    }
  },

  onShow() {
    this.loadProfile();
  },

  loadProfile() {
    const allPlots = plots.loadPlots();
    const allReminders = reminder.loadReminders();
    const region = storage.safeGet('userRegion', '未设置');
    const diaries = storage.safeGet('diaries', []);

    let totalCrops = 0;
    allPlots.forEach(plot => {
      if (plot.crops) {
        totalCrops += plot.crops.length;
      }
    });

    const pendingReminders = allReminders.filter(r => r.status === 'pending');

    this.setData({
      region: region,
      stats: {
        plots: allPlots.length,
        crops: totalCrops,
        reminders: pendingReminders.length
      }
    });
  },

  goToRegion() {
    wx.navigateTo({
      url: '/pages/region/region'
    });
  },

  goToOnboarding() {
    wx.navigateTo({
      url: '/pages/onboarding/onboarding'
    });
  },

  goToReminder() {
    wx.navigateTo({
      url: '/pages/reminder/reminder'
    });
  },

  clearCache() {
    wx.showModal({
      title: '清理缓存',
      content: '确定要清理所有本地缓存数据吗？',
      success: (res) => {
        if (res.confirm) {
          storage.clearAll();
          wx.showToast({
            title: '清理成功',
            icon: 'success'
          });
          this.loadProfile();
        }
      }
    });
  },

  showAbout() {
    wx.showModal({
      title: '关于农事通',
      content: '农事通是一款专注于农业生产的智能小程序，提供24节气查询、作物管理、农事提醒等功能，帮助农民科学种田，提高农业生产效率。\n\n版本：1.0.0',
      showCancel: false
    });
  }
});
