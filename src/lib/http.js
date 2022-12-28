import app from "@/main";

/**
 * 发送一个Get请求
 * @param {string} url 目标URL
 * @param {*} data 数据
 */
const get = (url, data = {}) => {
  return new Promise((resolve, reject) => {
    app.$http
      .get(url, data)
      .then((res) => {
        resolve(res.data);
      })
      .catch((err) => {
        reject(err.data);
      });
  });
};

/**
 * 发送一个Post请求
 * @param {string} url 目标URL
 * @param {*} data 数据
 */
const post = (url, data = {}) => {
  return new Promise((resolve, reject) => {
    app.$http
      .post(url, data)
      .then((res) => {
        resolve(res.data);
      })
      .catch((err) => {
        reject(err.data);
      });
  });
};

export { get, post };
