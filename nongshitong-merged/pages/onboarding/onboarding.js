const plots = require('../../utils/plots.js');
const crops = require('../../utils/crops.js');

Page({
  data: {
    currentStep: 1,
    stepTitle: '基本信息',
    plotForm: {
      name: '',
      area: '',
      unit: '亩',
      soilType: '普通土',
      irrigationType: '自然降水'
    },
    soilTypes: plots.getSoilTypes(),
    irrigationTypes: plots.getIrrigationTypes(),
    areaUnits: plots.getAreaUnits(),
    soilTypeIndex: 0,
    irrigationIndex: 0,
    unitIndex: 0,
    allCrops: crops.getAllCrops(),
    selectedCrops: []
  },

  onNameInput(e) {
    this.setData({
      'plotForm.name': e.detail.value
    });
  },

  onAreaInput(e) {
    this.setData({
      'plotForm.area': e.detail.value
    });
  },

  onUnitChange(e) {
    const unit = this.data.areaUnits[e.detail.value];
    this.setData({
      unitIndex: e.detail.value,
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

  toggleCrop(e) {
    const id = e.currentTarget.dataset.id;
    const selected = this.data.selectedCrops;
    const index = selected.indexOf(id);

    if (index > -1) {
      selected.splice(index, 1);
    } else {
      selected.push(id);
    }

    this.setData({
      selectedCrops: selected
    });
  },

  prevStep() {
    const step = this.data.currentStep - 1;
    this.setData({
      currentStep: step,
      stepTitle: this.getStepTitle(step)
    });
  },

  nextStep() {
    if (this.data.currentStep === 1) {
      if (!this.data.plotForm.name) {
        wx.showToast({ title: '请输入地块名称', icon: 'none' });
        return;
      }
    }

    const step = this.data.currentStep + 1;
    this.setData({
      currentStep: step,
      stepTitle: this.getStepTitle(step)
    });
  },

  getStepTitle(step) {
    const titles = {
      1: '基本信息',
      2: '环境设置',
      3: '选择作物'
    };
    return titles[step];
  },

  complete() {
    const form = this.data.plotForm;
    const selectedCrops = this.data.selectedCrops.map(id => {
      const crop = crops.getCropById(id);
      return {
        cropId: id,
        cropName: crop ? crop.name : id,
        addedAt: new Date().toISOString()
      };
    });

    const newPlot = plots.addPlot({
      ...form,
      crops: selectedCrops,
      status: selectedCrops.length > 0 ? 'active' : 'idle'
    });

    wx.showToast({
      title: '创建成功',
      icon: 'success'
    });

    setTimeout(() => {
      wx.switchTab({
        url: '/pages/my-field/my-field'
      });
    }, 1500);
  }
});
