import app from "@/main";

/**
 * 发送一个Get请求
 * @param {string} url
 * @param {*} data
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
    // app.$http
    //   .get(url, data)
    //   .then((res) => {
    //     console.log(res);
    //     return res;
    //   })
    //   .catch((e) => {
    //     return undefined;
    //   });
  });
};

/**
 * 发送一个Post请求
 * @param {string} url
 * @param {*} data
 */
const post = (url, data = {}) => {
  // app.$http
  //   .post(url, data)
  //   .then((res) => {
  //     console.log(res.data);
  //     return res.data;
  //   })
  //   .catch((e) => {
  //     return undefined;
  //   });
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
