import apiClient from './index.js';

const recordsApi = {
  getRecords: async (params) => {
    try {
      const response = await apiClient.get('/records', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  createRecord: async (record) => {
    try {
      const response = await apiClient.post('/records', record);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  updateRecord: async (id, record) => {
    try {
      const response = await apiClient.put(`/records/${id}`, record);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  deleteRecord: async (id) => {
    try {
      const response = await apiClient.delete(`/records/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  getGrades: async (params) => {
    try {
      const response = await apiClient.get('/records/grades', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default recordsApi;