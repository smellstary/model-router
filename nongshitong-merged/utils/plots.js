const DEFAULT_PLOT = {
  id: '',
  name: '我的田',
  area: 0,
  unit: '亩',
  soilType: '普通土',
  irrigationType: '自然降水',
  crops: [],
  status: 'idle'
};

const SOIL_TYPES = ['普通土', '沙质土', '黏质土', '壤土', '盐碱土', '酸性土'];
const IRRIGATION_TYPES = ['自然降水', '漫灌', '滴灌', '喷灌', '沟灌'];
const AREA_UNITS = ['亩', '平方米', '公顷'];

function getDefaultPlot() {
  return {
    ...DEFAULT_PLOT,
    id: 'plot_' + Date.now()
  };
}

function getSoilTypes() {
  return SOIL_TYPES;
}

function getIrrigationTypes() {
  return IRRIGATION_TYPES;
}

function getAreaUnits() {
  return AREA_UNITS;
}

function savePlots(plots) {
  const storage = require('./storage.js');
  storage.safeSet('plots', plots);
}

function loadPlots() {
  const storage = require('./storage.js');
  return storage.safeGet('plots', []);
}

function addPlot(plot) {
  const plots = loadPlots();
  const newPlot = {
    ...getDefaultPlot(),
    ...plot,
    id: 'plot_' + Date.now()
  };
  plots.push(newPlot);
  savePlots(plots);
  return newPlot;
}

function updatePlot(id, updates) {
  const plots = loadPlots();
  const index = plots.findIndex(p => p.id === id);
  if (index !== -1) {
    plots[index] = { ...plots[index], ...updates };
    savePlots(plots);
    return plots[index];
  }
  return null;
}

function deletePlot(id) {
  const plots = loadPlots();
  const filtered = plots.filter(p => p.id !== id);
  savePlots(filtered);
  return filtered;
}

function getPlotById(id) {
  const plots = loadPlots();
  return plots.find(p => p.id === id);
}

module.exports = {
  getDefaultPlot,
  getSoilTypes,
  getIrrigationTypes,
  getAreaUnits,
  savePlots,
  loadPlots,
  addPlot,
  updatePlot,
  deletePlot,
  getPlotById
}
