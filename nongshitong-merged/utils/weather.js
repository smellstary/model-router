const PROVINCES_WITH_DATA = [
  '北京', '天津', '河北', '山西', '内蒙古',
  '辽宁', '吉林', '黑龙江',
  '上海', '江苏', '浙江', '安徽', '福建', '江西',
  '山东', '河南', '湖北', '湖南', '广东', '广西', '海南',
  '重庆', '四川', '贵州', '云南', '西藏',
  '陕西', '甘肃', '青海', '宁夏', '新疆'
];

let cachedWeather = null;
let cacheTime = 0;
const CACHE_DURATION = 30 * 60 * 1000;

function isProvinceSupported(province) {
  return PROVINCES_WITH_DATA.some(p => province && province.includes(p));
}

function filterWeatherByProvince(weatherData, province) {
  if (!province || isProvinceSupported(province)) {
    return weatherData;
  }
  return {
    ...weatherData,
    description: '该地区天气数据暂不可用'
  };
}

async function getWeather(latitude, longitude, retryCount = 0) {
  const MAX_RETRIES = 3;
  const TIMEOUT = 10000;

  if (cachedWeather && (Date.now() - cacheTime) < CACHE_DURATION) {
    return cachedWeather;
  }

  try {
    const weatherData = await requestWeather(latitude, longitude, TIMEOUT);
    cachedWeather = weatherData;
    cacheTime = Date.now();
    return weatherData;
  } catch (error) {
    if (retryCount < MAX_RETRIES) {
      await sleep(1000 * (retryCount + 1));
      return getWeather(latitude, longitude, retryCount + 1);
    }
    return getDefaultWeather();
  }
}

function requestWeather(latitude, longitude, timeout) {
  return new Promise((resolve, reject) => {
    const requestTask = wx.request({
      url: 'https://api.example.com/weather',
      data: {
        latitude,
        longitude
      },
      method: 'GET',
      timeout: timeout,
      success: (res) => {
        if (res.statusCode === 200 && res.data) {
          resolve(processWeatherData(res.data));
        } else {
          reject(new Error('Weather request failed'));
        }
      },
      fail: (err) => {
        reject(err);
      }
    });

    setTimeout(() => {
      requestTask.abort();
      reject(new Error('Weather request timeout'));
    }, timeout);
  });
}

function processWeatherData(rawData) {
  return {
    temperature: rawData.temperature || 20,
    humidity: rawData.humidity || 60,
    weather: rawData.weather || '晴',
    windSpeed: rawData.windSpeed || 3,
    windDirection: rawData.windDirection || '北风',
    aqi: rawData.aqi || 50,
    aqiLevel: rawData.aqiLevel || '优',
    forecast: rawData.forecast || [],
    updateTime: new Date().toLocaleString('zh-CN')
  };
}

function getDefaultWeather() {
  return {
    temperature: '--',
    humidity: '--',
    weather: '暂无数据',
    windSpeed: '--',
    windDirection: '--',
    aqi: '--',
    aqiLevel: '--',
    forecast: [],
    updateTime: '--',
    isDefault: true
  };
}

function getWeatherIcon(weather) {
  const iconMap = {
    '晴': '☀️',
    '多云': '⛅',
    '阴': '☁️',
    '小雨': '🌧️',
    '中雨': '🌧️',
    '大雨': '⛈️',
    '雷阵雨': '⛈️',
    '小雪': '🌨️',
    '中雪': '❄️',
    '大雪': '❄️',
    '雾': '🌫️',
    '霾': '🌫️'
  };
  return iconMap[weather] || '🌤️';
}

function getWeatherAdvice(temperature, weather) {
  const advices = [];

  if (temperature < 5) {
    advices.push('气温较低，注意防寒保暖');
  } else if (temperature > 35) {
    advices.push('高温预警，注意防暑降温');
  }

  if (weather.includes('雨')) {
    advices.push('有降水，请注意田间排水');
  }

  if (weather.includes('雪')) {
    advices.push('有降雪，注意作物防冻');
  }

  if (advices.length === 0) {
    advices.push('天气适宜，适合农事活动');
  }

  return advices;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function clearCache() {
  cachedWeather = null;
  cacheTime = 0;
}

module.exports = {
  getWeather,
  isProvinceSupported,
  filterWeatherByProvince,
  getWeatherIcon,
  getWeatherAdvice,
  clearCache,
  PROVINCES_WITH_DATA
}
