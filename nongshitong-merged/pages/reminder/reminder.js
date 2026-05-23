const reminder = require('../../utils/reminder.js');
const plots = require('../../utils/plots.js');
const solarTerms = require('../../utils/solarTerms.js');

Page({
  data: {
    reminders: [],
    filteredReminders: [],
    activeTab: 'all',
    pendingCount: 0,
    completedCount: 0,
    currentSolarTerm: {},
    showModal: false,
    form: {
      content: '',
      date: '',
      time: '08:00'
    }
  },

  onShow() {
    this.loadData();
  },

  loadData() {
    const allReminders = reminder.loadReminders();
    const { currentTerm } = solarTerms.getCurrentSolarTerm();

    const pending = allReminders.filter(r => r.status === 'pending');
    const completed = allReminders.filter(r => r.status === 'completed');

    this.setData({
      reminders: allReminders,
      pendingCount: pending.length,
      completedCount: completed.length,
      currentSolarTerm: currentTerm || {}
    });

    this.filterReminders();
  },

  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({ activeTab: tab });
    this.filterReminders();
  },

  filterReminders() {
    let filtered = this.data.reminders;

    if (this.data.activeTab === 'pending') {
      filtered = filtered.filter(r => r.status === 'pending');
    } else if (this.data.activeTab === 'completed') {
      filtered = filtered.filter(r => r.status === 'completed');
    }

    this.setData({ filteredReminders: filtered });
  },

  generateReminders() {
    const plotsData = plots.loadPlots();
    const storage = require('../../utils/storage.js');
    const region = storage.safeGet('userRegion');

    const generated = reminder.generateReminders(plotsData, region);

    const existingReminders = reminder.loadReminders();
    const existingIds = new Set(existingReminders.map(r => 
      `${r.plotId}_${r.cropId}_${r.solarTerm}`
    ));

    const newReminders = generated.filter(g => {
      const key = `${g.plotId}_${g.cropId}_${g.solarTerm}`;
      return !existingIds.has(key);
    });

    if (newReminders.length === 0) {
      wx.showToast({
        title: '已是最新提醒',
        icon: 'none'
      });
      return;
    }

    newReminders.forEach(r => reminder.addReminder(r));

    this.loadData();

    wx.showToast({
      title: `生成${newReminders.length}条提醒`,
      icon: 'success'
    });
  },

  toggleStatus(e) {
    const id = e.currentTarget.dataset.id;
    const item = this.data.reminders.find(r => r.id === id);

    if (item) {
      const newStatus = item.status === 'pending' ? 'completed' : 'pending';
      reminder.updateReminder(id, { status: newStatus });
      this.loadData();
    }
  },

  deleteReminder(e) {
    const id = e.currentTarget.dataset.id;

    wx.showModal({
      title: '确认删除',
      content: '确定要删除这条提醒吗？',
      success: (res) => {
        if (res.confirm) {
          reminder.deleteReminder(id);
          this.loadData();
          wx.showToast({
            title: '已删除',
            icon: 'success'
          });
        }
      }
    });
  },

  showAddReminder() {
    const today = new Date();
    const dateStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

    this.setData({
      showModal: true,
      form: {
        content: '',
        date: dateStr,
        time: '08:00'
      }
    });
  },

  closeModal() {
    this.setData({ showModal: false });
  },

  stopPropagation() {},

  onContentInput(e) {
    this.setData({
      'form.content': e.detail.value
    });
  },

  onDateChange(e) {
    this.setData({
      'form.date': e.detail.value
    });
  },

  onTimeChange(e) {
    this.setData({
      'form.time': e.detail.value
    });
  },

  submitReminder() {
    const form = this.data.form;

    if (!form.content) {
      wx.showToast({
        title: '请输入提醒内容',
        icon: 'none'
      });
      return;
    }

    const storage = require('../../utils/storage.js');
    const region = storage.safeGet('userRegion', '通用');

    const newReminder = {
      plotId: null,
      plotName: region,
      cropId: null,
      cropName: null,
      stage: '自定义',
      solarTerm: '',
      content: form.content,
      date: form.date,
      time: form.time,
      type: 'manual'
    };

    reminder.addReminder(newReminder);
    this.loadData();
    this.closeModal();

    wx.showToast({
      title: '添加成功',
      icon: 'success'
    });
  }
});
