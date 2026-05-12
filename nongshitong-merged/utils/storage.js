function safeGet(key, defaultValue = null) {
  try {
    const value = wx.getStorageSync(key);
    return value !== '' ? value : defaultValue;
  } catch (e) {
    console.error('safeGet error:', e);
    return defaultValue;
  }
}

function safeSet(key, value) {
  try {
    wx.setStorageSync(key, value);
    return true;
  } catch (e) {
    console.error('safeSet error:', e);
    return false;
  }
}

function safeRemove(key) {
  try {
    wx.removeStorageSync(key);
    return true;
  } catch (e) {
    console.error('safeRemove error:', e);
    return false;
  }
}

function clearAll() {
  try {
    wx.clearStorageSync();
    return true;
  } catch (e) {
    console.error('clearAll error:', e);
    return false;
  }
}

module.exports = {
  safeGet,
  safeSet,
  safeRemove,
  clearAll
}
