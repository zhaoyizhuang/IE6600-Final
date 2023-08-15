import api from "./api";

export default {
  async getStock(id, interval) {
    const response = await api.get(`stock/${id}`, {
      params: { interval },
    });
    return response.data;
  },
  async getCloseDataStock(id, interval) {
    const response = await api.get(`stock/${id}/close`, {
      params: { interval },
    });
    return response.data;
  },
  async getSignals(id) {
    const response = await api.get(`stock/${id}/signals`);
    return response.data;
  },
};
