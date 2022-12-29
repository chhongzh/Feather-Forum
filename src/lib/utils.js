import { useTitle } from "@vueuse/core";
import { ElNotification } from "element-plus";
/**
 * 设置题目
 * @param {string} title 题目
 */
const setWindowTitle = (title) => {
  useTitle(title);
};

/**
 * 打开一个Notification
 * @param {string} title 需要弹出的题目
 * @param {string} content 需要显示的内容
 */
const makeNotification = (title, content) => {
  ElNotification({
    title: title,
    message: content,
    position: "bottom-left",
  });
};

export { setWindowTitle, makeNotification };
