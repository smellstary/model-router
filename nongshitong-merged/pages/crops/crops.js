const crops = require('../../utils/crops.js');

Page({
  data: {
    allCrops: [],
    filteredCrops: [],
    categories: [],
    selectedCategory: '全部',
    searchKey: ''
  },

  onLoad() {
    this.loadCrops();
  },

  loadCrops() {
    const allCrops = crops.getAllCrops();
    const categories = ['全部', ...crops.getCropCategories()];

    this.setData({
      allCrops,
      filteredCrops: allCrops,
      categories
    });
  },

  selectCategory(e) {
    const category = e.currentTarget.dataset.category;
    this.setData({ selectedCategory: category });
    this.filterCrops();
  },

  onSearch(e) {
    const searchKey = e.detail.value;
    this.setData({ searchKey });
    this.filterCrops();
  },

  filterCrops() {
    let filtered = this.data.allCrops;

    if (this.data.selectedCategory !== '全部') {
      filtered = filtered.filter(c => c.category === this.data.selectedCategory);
    }

    if (this.data.searchKey) {
      const key = this.data.searchKey.toLowerCase();
      filtered = filtered.filter(c => 
        c.name.toLowerCase().includes(key) ||
        c.category.toLowerCase().includes(key)
      );
    }

    this.setData({ filteredCrops: filtered });
  },

  goToDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/crop-detail/crop-detail?id=${id}`
    });
  }
});
