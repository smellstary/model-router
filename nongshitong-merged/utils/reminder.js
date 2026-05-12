const solarTerms = require('./solarTerms.js');
const crops = require('./crops.js');
const plots = require('./plots.js');

function generateReminders(plotsData, region) {
  const reminders = [];
  const { currentTerm } = solarTerms.getCurrentSolarTerm();

  if (!currentTerm) return reminders;

  const currentSolarTermName = currentTerm.name;

  plotsData.forEach(plot => {
    if (plot.crops && plot.crops.length > 0) {
      plot.crops.forEach(plotCrop => {
        const stageInfo = crops.getCropStageBySolarTerm(plotCrop.cropId, currentSolarTermName);
        if (stageInfo) {
          reminders.push({
            id: 'reminder_' + Date.now() + '_' + plotCrop.cropId,
            plotId: plot.id,
            plotName: plot.name,
            cropId: plotCrop.cropId,
            cropName: plotCrop.cropName,
            stage: stageInfo.name,
            solarTerm: currentSolarTermName,
            content: `${stageInfo.description}`,
            date: formatDate(new Date()),
            time: '08:00',
            type: 'auto',
            status: 'pending'
          });
        }
      });
    }
  });

  const seasonalTips = getSeasonalTips(currentSolarTermName);
  seasonalTips.forEach(tip => {
    reminders.push({
      id: 'reminder_' + Date.now() + '_seasonal_' + reminders.length,
      plotId: null,
      plotName: '通用',
      cropId: null,
      cropName: null,
      stage: '季节提醒',
      solarTerm: currentSolarTermName,
      content: tip,
      date: formatDate(new Date()),
      time: '09:00',
      type: 'seasonal',
      status: 'pending'
    });
  });

  return reminders;
}

function getSeasonalTips(solarTermName) {
  const tipsMap = {
    '立春': ['开始准备春耕物资', '检修农具', '储备种子肥料'],
    '雨水': ['注意防涝排水', '麦田管理', '准备育秧'],
    '惊蛰': ['春耕全面展开', '防治病虫害', '果园管理'],
    '春分': ['早稻播种', '小麦追肥', '春耕大忙'],
    '清明': ['插秧播种', '春茶采摘', '防寒保温'],
    '谷雨': ['玉米播种', '棉花播种', '春播作物管理'],
    '立夏': ['油菜收获', '早稻管理', '蔬菜定植'],
    '小满': ['小麦灌浆', '水稻分蘖', '田间管理'],
    '芒种': ['小麦收割', '夏播作物', '抢收抢种'],
    '夏至': ['中耕除草', '防旱防涝', '作物管理'],
    '小暑': ['早稻管理', '棉花管理', '防汛抗旱'],
    '大暑': ['双季早稻收割', '防暑降温', '病虫害防治'],
    '立秋': ['晚稻管理', '秋菜播种', '果园管理'],
    '处暑': ['中稻管理', '秋收准备', '病虫害防治'],
    '白露': ['晚稻管理', '秋茶采摘', '干燥储藏'],
    '秋分': ['秋收大忙', '小麦播种', '果树管理'],
    '寒露': ['晚稻收割', '小麦播种', '秋耕'],
    '霜降': ['收获完毕', '秋耕深翻', '农田水利'],
    '立冬': ['冬小麦管理', '果树防寒', '农具保养'],
    '小雪': ['农田基本建设', '兴修水利', '积肥造肥'],
    '大雪': ['防寒保暖', '温室管理', '畜牧防冻'],
    '冬至': ['温室蔬菜', '果树修剪', '总结当年'],
    '小寒': ['农闲时节', '农田管理', '学习技术'],
    '大寒': ['制定计划', '购买物资', '准备春耕']
  };

  return tipsMap[solarTermName] || ['注意天气变化', '做好田间管理'];
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function saveReminders(reminders) {
  const storage = require('./storage.js');
  storage.safeSet('reminders', reminders);
}

function loadReminders() {
  const storage = require('./storage.js');
  return storage.safeGet('reminders', []);
}

function addReminder(reminder) {
  const reminders = loadReminders();
  const newReminder = {
    ...reminder,
    id: 'reminder_' + Date.now(),
    status: 'pending'
  };
  reminders.unshift(newReminder);
  saveReminders(reminders);
  return newReminder;
}

function updateReminder(id, updates) {
  const reminders = loadReminders();
  const index = reminders.findIndex(r => r.id === id);
  if (index !== -1) {
    reminders[index] = { ...reminders[index], ...updates };
    saveReminders(reminders);
    return reminders[index];
  }
  return null;
}

function deleteReminder(id) {
  const reminders = loadReminders();
  const filtered = reminders.filter(r => r.id !== id);
  saveReminders(filtered);
  return filtered;
}

function markReminderComplete(id) {
  return updateReminder(id, { status: 'completed', completedAt: formatDate(new Date()) });
}

module.exports = {
  generateReminders,
  getSeasonalTips,
  saveReminders,
  loadReminders,
  addReminder,
  updateReminder,
  deleteReminder,
  markReminderComplete
}
