import { get, post } from "@/lib/http";
import apiRoute from "@/config/apiRoute";

/**
 * 获取Authkey信息
 * @param {string} authkey 需要查询的Authkey
 * @returns
 */
const getAuthkeyInfo = (authkey) => {
  return post(apiRoute.api_user_info, { authkey: authkey });
};

/**
 * 验证Authkey是否有效
 * @param {string} authkey 需要查询的Authkey
 * @returns
 */
const validateAuthkey = (authkey) => {
  return post(apiRoute.api_authkey_v, { authkey: authkey });
};

/**
 * 获取本地的Authkey
 * @returns 返回获取的Authkey
 */
const getLocalAuthkey = () => {
  return globalThis.localStorage.getItem("authkey");
};

/**
 * 删除本地的authkey
 */
const delLocalAuthkey = () => {
  globalThis.localStorage.removeItem("authkey");
};

const setLocalAuthkey = (authkey) => {
  globalThis.localStorage.setItem("authkey", authkey);
};

export {
  getAuthkeyInfo,
  validateAuthkey,
  getLocalAuthkey,
  delLocalAuthkey,
  setLocalAuthkey,
};
