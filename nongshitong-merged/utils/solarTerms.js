const SOLAR_TERMS = [
  { name: '立春', month: 2, day: 3, description: '春季开始，万物复苏', icon: '🌱' },
  { name: '雨水', month: 2, day: 18, description: '降雨开始，雨量渐增', icon: '🌧️' },
  { name: '惊蛰', month: 3, day: 5, description: '春雷惊醒蛰虫', icon: '⚡' },
  { name: '春分', month: 3, day: 20, description: '昼夜平分，春季过半', icon: '🌸' },
  { name: '清明', month: 4, day: 4, description: '天清气明，春暖花开', icon: '🌿' },
  { name: '谷雨', month: 4, day: 19, description: '雨生百谷，播种时节', icon: '🌾' },
  { name: '立夏', month: 5, day: 5, description: '夏季开始，万物繁茂', icon: '☀️' },
  { name: '小满', month: 5, day: 20, description: '小麦籽粒渐满', icon: '🌾' },
  { name: '芒种', month: 6, day: 5, description: '有芒作物成熟，抢收抢种', icon: '🌾' },
  { name: '夏至', month: 6, day: 21, description: '白昼最长，阳气至极', icon: '🌻' },
  { name: '小暑', month: 7, day: 6, description: '暑气渐盛', icon: '🔥' },
  { name: '大暑', month: 7, day: 22, description: '一年最热时节', icon: '🌡️' },
  { name: '立秋', month: 8, day: 7, description: '秋季开始，暑去凉来', icon: '🍂' },
  { name: '处暑', month: 8, day: 22, description: '暑气消退', icon: '🍃' },
  { name: '白露', month: 9, day: 7, description: '露凝而白，秋意渐浓', icon: '💧' },
  { name: '秋分', month: 9, day: 22, description: '昼夜平分，秋季过半', icon: '🌕' },
  { name: '寒露', month: 10, day: 8, description: '露气寒冷，秋季深入', icon: '🍁' },
  { name: '霜降', month: 10, day: 23, description: '天气渐冷，开始降霜', icon: '❄️' },
  { name: '立冬', month: 11, day: 7, description: '冬季开始，万物收藏', icon: '🌨️' },
  { name: '小雪', month: 11, day: 22, description: '开始降雪，雪量尚小', icon: '🌨️' },
  { name: '大雪', month: 12, day: 7, description: '雪量增大，银装素裹', icon: '❄️' },
  { name: '冬至', month: 12, day: 21, description: '白昼最短，阴极阳生', icon: '🌑' },
  { name: '小寒', month: 1, day: 5, description: '气候渐冷，尚未极寒', icon: '🌬️' },
  { name: '大寒', month: 1, day: 20, description: '一年最冷时节', icon: '🥶' }
];

function getCurrentSolarTerm() {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const day = now.getDate();

  let currentTerm = null;
  let nextTerm = null;

  const sortedTerms = [...SOLAR_TERMS].sort((a, b) => {
    if (a.month !== b.month) return a.month - b.month;
    return a.day - b.day;
  });

  for (let i = 0; i < sortedTerms.length; i++) {
    const term = sortedTerms[i];
    const termDate = new Date(year, term.month - 1, term.day);
    const currentDate = new Date(year, month - 1, day);

    if (i === 0 && currentDate < termDate) {
      const prevYear = year - 1;
      const prevTerm = sortedTerms[sortedTerms.length - 1];
      currentTerm = { ...prevTerm, year: prevYear };
      nextTerm = { ...term, year };
      break;
    }

    if (i === sortedTerms.length - 1) {
      if (currentDate >= termDate) {
        currentTerm = { ...term, year };
        nextTerm = { ...sortedTerms[0], year: year + 1 };
      } else {
        currentTerm = null;
        nextTerm = { ...term, year };
      }
      break;
    }

    const nextTermData = sortedTerms[i + 1];
    const nextTermDate = new Date(year, nextTermData.month - 1, nextTermData.day);

    if (currentDate >= termDate && currentDate < nextTermDate) {
      currentTerm = { ...term, year };
      nextTerm = { ...nextTermData, year };
      break;
    }
  }

  return { currentTerm, nextTerm };
}

function getSolarTermByDate(month, day) {
  return SOLAR_TERMS.find(t => t.month === month && t.day === day);
}

function getSolarTermsByMonth(month) {
  return SOLAR_TERMS.filter(t => t.month === month);
}

function getAllSolarTerms() {
  return SOLAR_TERMS;
}

function getSolarTermIndex(name) {
  return SOLAR_TERMS.findIndex(t => t.name === name);
}

function getSolarTermForYear(year) {
  return SOLAR_TERMS.map(term => ({
    ...term,
    year,
    date: new Date(year, term.month - 1, term.day)
  }));
}

module.exports = {
  getCurrentSolarTerm,
  getSolarTermByDate,
  getSolarTermsByMonth,
  getAllSolarTerms,
  getSolarTermIndex,
  getSolarTermForYear
}
