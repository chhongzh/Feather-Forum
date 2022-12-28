<template>
  <el-container>
    <el-affix>
      <el-header v-show="!$route.meta.hideHeader">
        <el-menu mode="horizontal" :ellipsis="false" :router="true" :default-active="$route.path">
          <el-menu-item index="/" style="font-size:14px">{{ config.forumName }}</el-menu-item>
          <el-sub-menu index="帖子">
            <template #title>{{ $t('message.post') }}</template>
            <el-menu-item index="/post/write">{{ $t('message.writePost') }}</el-menu-item>
            <el-menu-item index="/post">{{ $t('message.postList') }}</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="用户">
            <template #title>{{ $t('message.user') }}</template>
            <el-menu-item index="/user">{{ $t('message.userList') }}</el-menu-item>
          </el-sub-menu>
          <div class="flex-grow"></div>
          <el-menu-item v-show="!$store.state.login" index="/login">
            <el-space :size="5">
              {{ $t('message.login') }}
            </el-space>
          </el-menu-item>
          <el-menu-item v-show="!$store.state.login" index="/register">
            <el-space :size="5">
              {{ $t('message.register') }}
            </el-space>
          </el-menu-item>
          <el-menu-item v-show="$store.state.login" index="/my">{{ $store.state.name }}</el-menu-item>
        </el-menu>
      </el-header>
    </el-affix>
    <el-main>
      <div class="foot-space"></div>
      <div v-show="!($store.state.login || $route.meta.hideHeader)">
        <el-card>
          <div>
            <p>{{ $t('message.plzLogin') }}</p>
          </div>
        </el-card>
        <div class="foot-space"></div>
      </div>
      <!-- Router -->
      <router-view :key="$route.fullPath" />
      <!-- End router -->
    </el-main>
    <el-footer v-show="!$route.meta.hideFooter" class="little">
      <div class="foot-space"></div>
      <b>{{ userAgent }}</b>
      <el-row>
        <el-col :span="8">
          <p v-if="!config.hideFeather">"<b>{{ config.forumName }}</b>" 由 "<b>
              <el-link :underline="false" href="https://github.com/chhongzh/Feather-Forum">Feather Forum
              </el-link>
            </b>" 提供支持</p>
        </el-col>
        <el-col :span="8">
          <p>
            © Copyright <b>{{ new Date().getFullYear() }}</b> <b>{{ weblink }}</b> All Rights Reserved
          </p>
        </el-col>
        <el-col :span="8">
          <p>
            © <b>{{ new Date().getFullYear() }}</b> <b>{{ weblink }}</b> {{ $t('message.copyright') }}
          </p>
        </el-col>
      </el-row>
      <div class="foot-layout-right">
        <p>
          <el-link type="primary" @click="changeReload">{{ $t('message.reload') }}</el-link>
        </p>
      </div>

    </el-footer>
  </el-container>

  <el-dialog v-model="reloadDialog" :title="$t('message.reload') + '?'" width="30%">
    <span>{{ $t('message.sureReload') }}<br>{{ $t('message.dataLoss') }}</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="changeReload">{{ $t('message.cancel') }}</el-button>
        <el-button type="primary" @click="reload">{{ $t('message.reload') }}</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { setWindowTitle } from '@/lib/utils'
import cn from '@/i18n/cn'
</script>

<script>
import config from '@/config/web'
export default {
  data() {
    return {
      weblink: '',
      userAgent: '',
      reloadDialog: false,
    }
  },
  mounted() {
    // console.log(JSON.stringify(cn))
    console.log(JSON.parse('{"back": "返回", "backHome": "返回主页", "cancel": "取消", "continueTo": "继续前往", "copyright": "版权所有", "dataLoss": "未保存的数据将会丢失!", "fillThis": "填写此字段", "jumpTip": "跳转提示", "logged": "你已经登陆过了!", "login": "登录", "loginError": "登录失败,请检查网络连接!", "logout": "登出", "logoutDone": "登出成功", "missingArg": "参数缺失", "networkError": "网络错误", "newBlankAndBack": "在新标签页打开并返回", "newMembers": "新成员", "newPost": "新帖子", "noAccount": "没有账号?点我注册!", "noData": "没有数据", "notBelong": "不属于", "notFoundCheckUrl": "检查您是否拼错URL?", "notFoundTitle": "未找到您访问的路由记录", "notLogin": "未登录", "password": "密码", "plzLogin": "访客,请先登录", "post": "帖子", "postList": "帖子列表", "postTitle": "帖子标题", "register": "注册", "reload": "重新加载", "submit": "提交", "sureReload": "你确定重新加载吗?", "user": "用户", "userList": "用户列表", "username": "用户名"}'))

    if (config.webHost == 'auto') {
      this.weblink = window.location.hostname
    } else {
      this.weblink = config.webHost
    }

    this.userAgent = navigator.appName + ' ' + navigator.appCodeName + ' ' + navigator.appVersion
    var ak = localStorage.getItem('authkey')
    if (ak) { // 判断是否存在
      this.getAuthkeyInfo(ak).then((res) => { // 判断是否存活
        if (res.data.authkey) {
          this.logon = true
          this.uname = res.data.name
          this.$store.commit('login')
          this.$store.commit('name', res.data.name)
          localStorage.setItem('authkey', ak)
        } else {
          localStorage.removeItem('authkey')
          this.$store.commit('logout')
          this.$store.commit('name', '')
        }
      })
    }

    setWindowTitle(config.forumName) // 设置Title

    Notification.requestPermission((permission) => { }); // 申请权限

    addEventListener("visibilitychange", () => {
      if (document.hidden) {
        setWindowTitle("记得回来哦!")
      } else {
        setWindowTitle(config.forumName)
      }
    });

  },
  methods: {
    /**
     * 改变对话框状态
     */
    changeReload() {
      this.reloadDialog = !this.reloadDialog
    },
    /**
     * 重新加载页面
     */
    reload() {
      this.changeReload()
      window.location.reload()
    },
    /**
     * 
     * @param {string} url 目标URL
     * @param {*} data 数据
     */
    post(url, data) {
      return new Promise((resolve, reject) => {
        this.$http
          .post(url, data)
          .then((res) => {
            resolve(res.data);
          })
          .catch((err) => {
            reject(err.data);
          });
      });
    },
    /**
     * 获取Authkey信息
     * @param {string} authkey 需要查询的Authkey
     * @returns
     */
    getAuthkeyInfo(authkey) {
      return this.post("/api/user/info", { authkey: authkey });
    }
  },
}
</script>

<style>
body {
  width: 100%;
  height: 100%;
}

* {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
}

.flex-grow {
  flex-grow: 1;
}

.title {
  padding: 0;
  margin: 0 0 3px 0;
  font-size: 3.6rem;
  font-weight: 400;
  margin-right: auto;
  min-width: 0;
}

.top {
  margin-top: 12.5px;
}

.web-title {
  font-family: 'Minecraft';
  font-size: 78px;
}

.little {
  font-size: 14px;
  /* font-family: 'Minecraft'; */
}

.foot-space {
  margin-top: 14px;
}

.left-space {
  margin-left: 10px;
}

.alert {
  color: red
}

.foot-layout-right {
  text-align: right;
}

.h2 {
  font-size: 36px;
  margin-top: 0px;
  /* font- */
}

.mask {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  background-color: #ecf2fb;
  z-index: 0;
}

a {
  text-decoration: none;
}

.login-box {
  width: 400px;
}
</style>


