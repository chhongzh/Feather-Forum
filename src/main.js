import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementPlus from "element-plus";
import VueAxios from "vue-axios";
import Axios from "axios";
import NProgress from "nprogress";
import config from "./assets/js/config";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faCircleUser, faClipboard } from "@fortawesome/free-regular-svg-icons";

import "./assets/js/prism.js";

import "./assets/css/prism.css";
import "nprogress/nprogress.css";
import "element-plus/theme-chalk/dark/css-vars.css";
import "element-plus/dist/index.css";
import "./assets/css/editor.css";
import VMdEditor from "@kangc/v-md-editor/lib/codemirror-editor";
import "@kangc/v-md-editor/lib/style/codemirror-editor.css";
import githubTheme from "@kangc/v-md-editor/lib/theme/github.js";
import "@kangc/v-md-editor/lib/theme/style/github.css";
// import vuepressTheme from "@kangc/v-md-editor/lib/theme/vuepress.js";
// import "@kangc/v-md-editor/lib/theme/style/vuepress.css";

// highlightjs
import hljs from "highlight.js";

// codemirror 编辑器的相关资源
import Codemirror from "codemirror";
// mode
import "codemirror/mode/markdown/markdown";
import "codemirror/mode/javascript/javascript";
import "codemirror/mode/css/css";
import "codemirror/mode/htmlmixed/htmlmixed";
import "codemirror/mode/vue/vue";
// edit
import "codemirror/addon/edit/closebrackets";
import "codemirror/addon/edit/closetag";
import "codemirror/addon/edit/matchbrackets";
// placeholder
import "codemirror/addon/display/placeholder";
// active-line
import "codemirror/addon/selection/active-line";
// scrollbar
import "codemirror/addon/scroll/simplescrollbars";
import "codemirror/addon/scroll/simplescrollbars.css";
// style
import "codemirror/lib/codemirror.css";
import createTipPlugin from "@kangc/v-md-editor/lib/plugins/tip/index";
import "@kangc/v-md-editor/lib/plugins/tip/tip.css";
import createCopyCodePlugin from "@kangc/v-md-editor/lib/plugins/copy-code/index";
import "@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css";
VMdEditor.Codemirror = Codemirror;

VMdEditor.use(githubTheme, {
  Hljs: hljs,
});
VMdEditor.use(createTipPlugin());
VMdEditor.use(createCopyCodePlugin());

const app = createApp(App);

NProgress.configure({
  easing: "ease", // 动画方式
  speed: 500, // 递增进度条的速度
  showSpinner: true, // 是否显示加载ico
  trickleSpeed: 200, // 自动递增间隔
  minimum: 0.3, // 初始化时的最小百分比
});

// Axios.defaults.baseURL="http://192.168.3.33:14524"
Axios.defaults.baseURL = config.baseURL;

router.beforeEach((to, from, next) => {
  // 每次切换页面时，调用进度条
  NProgress.start();
  next();
});
router.afterEach(() => {
  NProgress.done();
});

library.add(faCircleUser, faClipboard);

app.use(store);
app.use(router);
app.use(ElementPlus);
app.use(VueAxios, Axios);
app.component("font-awesome-icon", FontAwesomeIcon);
app.use(VMdEditor);

app.mount("#app");