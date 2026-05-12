const solarTerms = require('../../utils/solarTerms.js');

Page({
  data: {
    currentYear: new Date().getFullYear(),
    viewMode: 'term',
    termsForYear: [],
    currentTerm: {},
    months: [],
    seasons: [],
    showDetail: false,
    selectedTerm: {}
  },

  onLoad() {
    this.loadTimeline();
  },

  loadTimeline() {
    const terms = solarTerms.getSolarTermForYear(this.data.currentYear);
    const { currentTerm } = solarTerms.getCurrentSolarTerm();

    this.setData({
      termsForYear: terms,
      currentTerm: currentTerm || {}
    });

    this.groupByMonth();
    this.groupBySeason();
  },

  groupByMonth() {
    const allTerms = solarTerms.getAllSolarTerms();
    const months = [];

    for (let i = 1; i <= 12; i++) {
      months.push(allTerms.filter(t => t.month === i));
    }

    this.setData({ months });
  },

  groupBySeason() {
    const terms = this.data.termsForYear;
    const seasons = [
      {
        name: '春季',
        icon: '🌸',
        terms: terms.filter(t => ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨'].includes(t.name))
      },
      {
        name: '夏季',
        icon: '☀️',
        terms: terms.filter(t => ['立夏', '小满', '芒种', '夏至', '小暑', '大暑'].includes(t.name))
      },
      {
        name: '秋季',
        icon: '🍂',
        terms: terms.filter(t => ['立秋', '处暑', '白露', '秋分', '寒露', '霜降'].includes(t.name))
      },
      {
        name: '冬季',
        icon: '❄️',
        terms: terms.filter(t => ['立冬', '小雪', '大雪', '冬至', '小寒', '大寒'].includes(t.name))
      }
    ];

    this.setData({ seasons });
  },

  prevYear() {
    const year = this.data.currentYear - 1;
    this.setData({ currentYear: year });
    this.loadTimeline();
  },

  nextYear() {
    const year = this.data.currentYear + 1;
    this.setData({ currentYear: year });
    this.loadTimeline();
  },

  switchView(e) {
    const mode = e.currentTarget.dataset.mode;
    this.setData({ viewMode: mode });
  },

  showMonthTerms(e) {
    const month = e.currentTarget.dataset.month;
    const monthTerms = this.data.months[month - 1];
    if (monthTerms && monthTerms.length > 0) {
      this.setData({
        showDetail: true,
        selectedTerm: { ...monthTerms[0], year: this.data.currentYear }
      });
    }
  },

  getFarmingTips(termName) {
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
    return tipsMap[termName] || ['注意天气变化', '做好田间管理'];
  },

  closeDetail() {
    this.setData({ showDetail: false });
  },

  stopPropagation() {}
});
