import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementPlus from "element-plus";
import VueAxios from "vue-axios";
import Axios from "axios";
import NProgress from "nprogress";
import config from "./assets/js/config";

import "nprogress/nprogress.css";
import "element-plus/theme-chalk/dark/css-vars.css";
import "element-plus/dist/index.css";
import VMdEditor from "@kangc/v-md-editor/lib/codemirror-editor";
import "@kangc/v-md-editor/lib/style/codemirror-editor.css";
import githubTheme from "@kangc/v-md-editor/lib/theme/github.js";
import "@kangc/v-md-editor/lib/theme/style/github.css";
import hljs from "highlight.js";

import Codemirror from "codemirror";
import "codemirror/mode/markdown/markdown";
import "codemirror/mode/javascript/javascript";
import "codemirror/mode/css/css";
import "codemirror/mode/htmlmixed/htmlmixed";
import "codemirror/mode/vue/vue";
import "codemirror/addon/edit/closebrackets";
import "codemirror/addon/edit/closetag";
import "codemirror/addon/edit/matchbrackets";
import "codemirror/addon/display/placeholder";
import "codemirror/addon/selection/active-line";
import "codemirror/addon/scroll/simplescrollbars";
import "codemirror/addon/scroll/simplescrollbars.css";
import "codemirror/lib/codemirror.css";

import createCopyCodePlugin from "@kangc/v-md-editor/lib/plugins/copy-code/index";
import "@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css";
import createTipPlugin from "@kangc/v-md-editor/lib/plugins/tip/index";
import "@kangc/v-md-editor/lib/plugins/tip/tip.css";
import createEmojiPlugin from "@kangc/v-md-editor/lib/plugins/emoji/index";
import "@kangc/v-md-editor/lib/plugins/emoji/emoji.css";
import createKatexPlugin from "@kangc/v-md-editor/lib/plugins/katex/cdn";
import createMermaidPlugin from "@kangc/v-md-editor/lib/plugins/mermaid/cdn";
import "@kangc/v-md-editor/lib/plugins/mermaid/mermaid.css";
import createTodoListPlugin from "@kangc/v-md-editor/lib/plugins/todo-list/index";
import "@kangc/v-md-editor/lib/plugins/todo-list/todo-list.css";
import createLineNumbertPlugin from "@kangc/v-md-editor/lib/plugins/line-number/index";
import createAlignPlugin from "@kangc/v-md-editor/lib/plugins/align";

VMdEditor.Codemirror = Codemirror;
VMdEditor.use(githubTheme, {
  Hljs: hljs,
});
VMdEditor.use(createTipPlugin());
VMdEditor.use(createCopyCodePlugin());
VMdEditor.use(createEmojiPlugin());
VMdEditor.use(createKatexPlugin());
VMdEditor.use(createMermaidPlugin());
VMdEditor.use(createTodoListPlugin());
VMdEditor.use(createLineNumbertPlugin());
VMdEditor.use(createAlignPlugin());

const app = createApp(App);

NProgress.configure({
  easing: "ease", // 动画方式
  speed: 500, // 递增进度条的速度
  showSpinner: true, // 是否显示加载ico
  trickleSpeed: 200, // 自动递增间隔
  minimum: 0.3, // 初始化时的最小百分比
});

Axios.defaults.baseURL = config.baseURL;

router.beforeEach((to, from, next) => {
  NProgress.start();
  next();
});
router.afterEach(() => {
  NProgress.done();
});

app.use(store);
app.use(router);
app.use(ElementPlus);
app.use(VueAxios, Axios);
app.use(VMdEditor);

app.mount("#app");
