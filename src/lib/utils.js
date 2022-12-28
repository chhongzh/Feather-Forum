import { useTitle } from "@vueuse/core";
/**
 * 设置题目
 * @param {string} title 题目
 */
const setWindowTitle = (title) => {
  useTitle(title);
};

export { setWindowTitle };
