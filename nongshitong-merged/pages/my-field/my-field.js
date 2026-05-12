const plots = require('../../utils/plots.js');
const storage = require('../../utils/storage.js');

Page({
  data: {
    plots: [],
    diaries: [],
    showModal: false,
    modalType: 'plot',
    soilTypes: plots.getSoilTypes(),
    irrigationTypes: plots.getIrrigationTypes(),
    areaUnits: plots.getAreaUnits(),
    soilTypeIndex: 0,
    irrigationIndex: 0,
    areaUnitIndex: 0,
    plotForm: {
      name: '',
      area: '',
      unit: '亩',
      soilType: '普通土',
      irrigationType: '自然降水'
    },
    diaryForm: {
      date: '',
      plotName: '',
      plotId: '',
      content: ''
    },
    diaryPlotIndex: 0
  },

  onShow() {
    this.loadData();
  },

  loadData() {
    const allPlots = plots.loadPlots();
    const diaries = storage.safeGet('diaries', []);

    this.setData({
      plots: allPlots,
      diaries: diaries.slice(0, 10)
    });
  },

  showAddPlot() {
    this.setData({
      showModal: true,
      modalType: 'plot',
      plotForm: {
        name: '',
        area: '',
        unit: '亩',
        soilType: '普通土',
        irrigationType: '自然降水'
      }
    });
  },

  showAddDiary() {
    if (this.data.plots.length === 0) {
      wx.showToast({
        title: '请先添加地块',
        icon: 'none'
      });
      return;
    }

    const today = new Date();
    const dateStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

    this.setData({
      showModal: true,
      modalType: 'diary',
      diaryForm: {
        date: dateStr,
        plotName: this.data.plots[0].name,
        plotId: this.data.plots[0].id,
        content: ''
      }
    });
  },

  closeModal() {
    this.setData({ showModal: false });
  },

  stopPropagation() {},

  onPlotNameInput(e) {
    this.setData({
      'plotForm.name': e.detail.value
    });
  },

  onPlotAreaInput(e) {
    this.setData({
      'plotForm.area': e.detail.value
    });
  },

  onUnitChange(e) {
    const unit = this.data.areaUnits[e.detail.value];
    this.setData({
      areaUnitIndex: e.detail.value,
      'plotForm.unit': unit
    });
  },

  onSoilTypeChange(e) {
    const soilType = this.data.soilTypes[e.detail.value];
    this.setData({
      soilTypeIndex: e.detail.value,
      'plotForm.soilType': soilType
    });
  },

  onIrrigationChange(e) {
    const irrigationType = this.data.irrigationTypes[e.detail.value];
    this.setData({
      irrigationIndex: e.detail.value,
      'plotForm.irrigationType': irrigationType
    });
  },

  onDiaryDateChange(e) {
    this.setData({
      'diaryForm.date': e.detail.value
    });
  },

  onDiaryPlotChange(e) {
    const plot = this.data.plots[e.detail.value];
    this.setData({
      diaryPlotIndex: e.detail.value,
      'diaryForm.plotName': plot.name,
      'diaryForm.plotId': plot.id
    });
  },

  onDiaryContentInput(e) {
    this.setData({
      'diaryForm.content': e.detail.value
    });
  },

  submitForm() {
    if (this.data.modalType === 'plot') {
      this.submitPlot();
    } else {
      this.submitDiary();
    }
  },

  submitPlot() {
    const form = this.data.plotForm;
    if (!form.name) {
      wx.showToast({ title: '请输入地块名称', icon: 'none' });
      return;
    }

    const newPlot = plots.addPlot(form);
    this.loadData();
    this.closeModal();

    wx.showToast({ title: '添加成功', icon: 'success' });
  },

  submitDiary() {
    const form = this.data.diaryForm;
    if (!form.content) {
      wx.showToast({ title: '请输入日记内容', icon: 'none' });
      return;
    }

    const diaries = storage.safeGet('diaries', []);
    const newDiary = {
      id: 'diary_' + Date.now(),
      ...form,
      createdAt: new Date().toISOString()
    };

    diaries.unshift(newDiary);
    storage.safeSet('diaries', diaries);

    this.loadData();
    this.closeModal();

    wx.showToast({ title: '保存成功', icon: 'success' });
  },

  goToPlotDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/my-field/my-field?plotId=${id}`
    });
  }
});
