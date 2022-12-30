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
      <div v-show="!(($store.state.login || $route.meta.hideHeader) || $route.meta.hideLoginTip)">
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
      <el-backtop />
    </el-main>
    <el-footer v-show="!$route.meta.hideFooter" class="little">
      <div class="foot-space"></div>
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
        <el-dropdown>
          <span class="el-dropdown-link">
            {{ $t('message.lang') }}
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="switchLang('cn')">简体中文</el-dropdown-item>
              <el-dropdown-item @click="switchLang('en')">English</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
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
</script>

<script>
import config from '@/config/web'
import { getLocalAuthkey, delLocalAuthkey, setLocalAuthkey } from './lib/auth';
import { makeNotification } from '@/lib/utils'
export default {
  data() {
    return {
      weblink: '',
      reloadDialog: false,
    }
  },
  mounted() {
    if (config.webHost == 'auto') {
      this.weblink = window.location.hostname
    } else {
      this.weblink = config.webHost
    }

    var ak = getLocalAuthkey()
    if (ak) { // 判断是否存在
      this.getAuthkeyInfo(ak).then((res) => { // 判断是否存活
        if (res.data.authkey) {
          this.logon = true
          this.uname = res.data.name
          this.$store.commit('login')
          this.$store.commit('name', res.data.name)
          setLocalAuthkey(ak)
        } else {
          delLocalAuthkey()
          this.$store.commit('logout')
          this.$store.commit('name', '')
        }
      })
    }

    setWindowTitle(config.forumName) // 设置Title

    Notification.requestPermission((permission) => {
      if (permission == 'denied') {
        makeNotification(this.$t('message.permission'), this.$t('message.permissionBlock'))
      } else if (permission == 'granted') {

      } else {
        makeNotification(this.$t('message.permission'), this.$t('message.permissionDefault'))
      }
    }); // 申请权限

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
    },
    /**
     * 更改语言
     * @param {string} lang 需要改变的语言
     */
    switchLang(lang) {
      this.$i18n.locale = lang
      makeNotification(this.$t('message.langTip'), this.$t('message.langMessage'))
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


