// 达人申请页
const { api } = require('../../../utils/api.js');

Page({
  data: {
    formData: {
      realName: '',
      phone: '',
      applyReason: '',
      intro: ''
    },
    region: [],
    regionIndex: [0, 0, 0],
    isSubmitting: false,
    provinces: [],
    cities: [],
    districts: [],
    provincesData: [],
    citiesData: {},
    districtsData: {}
  },

  onLoad() {
    this.loadRegionData();
  },

  loadRegionData() {
    wx.showLoading({ title: '加载中...' });
    
    wx.request({
      url: 'http://localhost:5000/api/region/data',
      method: 'GET',
      success: (res) => {
        wx.hideLoading();
        
        if (res.data.code === 200 && res.data.data && res.data.data.length > 0) {
          const regionData = res.data.data;
          
          const provincesData = regionData.map(p => ({ code: p.code, name: p.name }));
          const citiesData = {};
          const districtsData = {};
          
          regionData.forEach(province => {
            citiesData[province.code] = province.children.map(c => ({ code: c.code, name: c.name }));
            
            province.children.forEach(city => {
              districtsData[city.code] = city.children.map(d => ({ code: d.code, name: d.name }));
            });
          });
          
          const firstProvince = provincesData[0];
          let firstCities = [];
          let firstDistricts = [];
          
          if (firstProvince && citiesData[firstProvince.code]) {
            firstCities = citiesData[firstProvince.code];
            const firstCity = firstCities[0];
            if (firstCity && districtsData[firstCity.code]) {
              firstDistricts = districtsData[firstCity.code];
            }
          }
          
          this.setData({
            provinces: provincesData.map(p => p.name),
            provincesData: provincesData,
            citiesData: citiesData,
            districtsData: districtsData,
            cities: firstCities.map(c => c.name),
            districts: firstDistricts.map(d => d.name)
          });
        } else {
          wx.showToast({
            title: '地区数据为空',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: '加载地区数据失败',
          icon: 'none'
        });
      }
    });
  },

  onInputChange(e) {
    const { field } = e.currentTarget.dataset;
    const { value } = e.detail;
    
    this.setData({
      [`formData.${field}`]: value
    });
  },

  onRegionChange(e) {
    const value = e.detail.value;
    const { provinces, cities, districts } = this.data;
    
    if (value[0] >= 0 && value[1] >= 0 && value[2] >= 0) {
      this.setData({
        region: [provinces[value[0]], cities[value[1]], districts[value[2]]],
        regionIndex: value
      });
    }
  },

  onColumnChange(e) {
    const column = e.detail.column;
    const value = e.detail.value;
    const { provincesData, citiesData, districtsData, regionIndex } = this.data;
    
    if (column === 0) {
      const province = provincesData[value];
      if (!province) return;
      
      const newCities = citiesData[province.code] || [];
      const firstCity = newCities[0] || { code: '', name: '' };
      const newDistricts = districtsData[firstCity.code] || [];
      
      this.setData({
        cities: newCities.map(c => c.name),
        districts: newDistricts.map(d => d.name),
        regionIndex: [value, 0, 0]
      });
    } else if (column === 1) {
      const province = provincesData[regionIndex[0]];
      if (!province) return;
      
      const cities = citiesData[province.code] || [];
      const city = cities[value] || { code: '', name: '' };
      const newDistricts = districtsData[city.code] || [];
      
      this.setData({
        districts: newDistricts.map(d => d.name),
        regionIndex: [regionIndex[0], value, 0]
      });
    }
  },

  async submitApply() {
    if (this.data.isSubmitting) {
      return;
    }

    const { formData } = this.data;
    
    if (!formData.realName) {
      wx.showToast({
        title: '请输入真实姓名',
        icon: 'none'
      });
      return;
    }

    if (formData.realName.length < 2 || formData.realName.length > 20) {
      wx.showToast({
        title: '真实姓名需在2-20个字符之间',
        icon: 'none'
      });
      return;
    }

    if (!formData.phone) {
      wx.showToast({
        title: '请输入手机号码',
        icon: 'none'
      });
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      });
      return;
    }

    if (!formData.applyReason) {
      wx.showToast({
        title: '请输入申请理由',
        icon: 'none'
      });
      return;
    }

    if (formData.applyReason.length < 10 || formData.applyReason.length > 500) {
      wx.showToast({
        title: '申请理由需在10-500个字符之间',
        icon: 'none'
      });
      return;
    }

    this.setData({ isSubmitting: true });

    try {
      const params = {
        realName: formData.realName,
        phone: formData.phone,
        region: this.data.region.length > 0 ? `${this.data.region[0]} ${this.data.region[1]} ${this.data.region[2]}` : '',
        applyReason: formData.applyReason,
        intro: formData.intro
      };

      const res = await api.post('/api/user/talent/apply', params);

      wx.showToast({
        title: '申请提交成功',
        icon: 'success'
      });
      
      setTimeout(() => {
        wx.redirectTo({
          url: '/pages/talent/status/index'
        });
      }, 1500);
    } catch (error) {
      console.error('提交申请失败:', error);
      wx.showToast({
        title: '网络错误，请重试',
        icon: 'none'
      });
      this.setData({ isSubmitting: false });
    }
  }
});
