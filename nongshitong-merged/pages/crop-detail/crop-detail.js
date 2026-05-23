const crops = require('../../utils/crops.js');
const solarTerms = require('../../utils/solarTerms.js');

Page({
  data: {
    crop: {},
    currentSolarTerm: ''
  },

  onLoad(options) {
    if (options.id) {
      this.loadCrop(options.id);
    }
  },

  loadCrop(id) {
    const crop = crops.getCropById(id);
    if (crop) {
      const { currentTerm } = solarTerms.getCurrentSolarTerm();
      const stages = crop.stages.map(s => ({
        ...s,
        isCurrent: s.solarTerm === currentTerm?.name
      }));

      this.setData({
        crop: { ...crop, stages },
        currentSolarTerm: currentTerm?.name || ''
      });

      wx.setNavigationBarTitle({
        title: crop.name
      });
    }
  },

  addToMyField() {
    const app = getApp();
    const plots = require('../../utils/plots.js');
    const allPlots = plots.loadPlots();

    if (allPlots.length === 0) {
      wx.navigateTo({
        url: '/pages/onboarding/onboarding'
      });
      return;
    }

    const crop = this.data.crop;
    const plotId = allPlots[0].id;

    const cropData = {
      cropId: crop.id,
      cropName: crop.name,
      addedAt: new Date().toISOString()
    };

    const plot = allPlots.find(p => p.id === plotId);
    if (plot) {
      const existingCrops = plot.crops || [];
      const alreadyExists = existingCrops.some(c => c.cropId === crop.id);

      if (alreadyExists) {
        wx.showToast({
          title: '该作物已添加',
          icon: 'none'
        });
        return;
      }

      existingCrops.push(cropData);
      plots.updatePlot(plotId, { crops: existingCrops });

      wx.showToast({
        title: '添加成功',
        icon: 'success'
      });

      setTimeout(() => {
        wx.switchTab({
          url: '/pages/my-field/my-field'
        });
      }, 1500);
    }
  }
});
