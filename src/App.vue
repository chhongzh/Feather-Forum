<template>
  <el-container>
    <el-affix>
      <el-header>
        <el-menu mode="horizontal" :ellipsis="false" :router="true" :default-active="$route.path">
          <el-menu-item index="/" style="font-size:14px">{{ forumName }}</el-menu-item>
          <el-sub-menu index="帖子">
            <template #title>帖子</template>
            <el-menu-item index="/post/write">发布</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="用户">
            <template #title>用户</template>
            <el-menu-item index="/user">用户列表</el-menu-item>
          </el-sub-menu>
          <div class="flex-grow"></div>
          <el-menu-item v-show="!$store.state.login" index="/login">
            <el-space :size="5">
              登录
            </el-space>
          </el-menu-item>
          <el-menu-item v-show="!$store.state.login" index="/register">
            <el-space :size="5">
              注册
            </el-space>
          </el-menu-item>
          <el-menu-item v-show="$store.state.login" index="/my">{{ $store.state.name }}</el-menu-item>
        </el-menu>
      </el-header>
    </el-affix>
    <el-main>
      <div class="foot-space"></div>
      <div v-show="!$store.state.login">
        <el-card>
          <div>
            <p>访客,请先登录</p>
          </div>
        </el-card>
        <div class="foot-space"></div>
      </div>
      <!-- Router -->
      <router-view :key="$route.fullPath" />
      <!-- End router -->
    </el-main>
    <el-footer class="little">
      <div class="foot-space"></div>
      <b>{{ userAgent }}</b>
      <el-row>
        <el-col :span="8">
          <p v-if="!hideFeather">"<b>{{ forumName }}</b>" 由 "<b>
              <el-link :underline="false" href="https://github.com/chhongzh/Feather-Forum">Feather Forum
              </el-link>
            </b>" 提供支持</p>
        </el-col>
        <el-col :span="8">
          <p>
            © Copyright <b>{{ year }}</b> <b>{{ weblink }}</b> All Rights Reserved
          </p>
        </el-col>
        <el-col :span="8">
          <p>
            © <b>{{ year }}</b> <b>{{ weblink }}</b> 版权所有
          </p>
        </el-col>
      </el-row>
      <div class="foot-layout-right">
        <p>
          <router-link to="/help">
            <el-link type="primary">帮助</el-link>
          </router-link>
          &nbsp;
          <el-link type="primary" @click="changeReload">重新加载</el-link>
        </p>
      </div>

    </el-footer>
  </el-container>

  <el-dialog v-model="reloadDialog" title="重新加载?" width="30%">
    <span>你确定要重新加载吗？<br>未保存的数据将会丢失!</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="unreload">取消</el-button>
        <el-button type="primary" @click="reload">重新加载</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { useTitle } from '@vueuse/core'
</script>

<script>
import config from './assets/js/config.js'
export default {
  data() {
    return {
      year: 1970,
      weblink: '',
      switchModel: '',
      userAgent: '',
      forumName: config.forumName,
      logon: false,
      uname: '',
      hideFeather: false,
      reloadDialog: false,
      loginDialog: true,
      registerDialog: false
    }
  },
  mounted() {
    if (!localStorage.getItem('accept')) {
      this.$alert('您使用本网站必须同意 "<b>隐私条款</b>" 以及 "<b>Cookie协议</b>" <br />继续使用则代表同意本条款<br /> 如果您不同意,请关闭本网页', '条款与协议', {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '我接受',
        callback: (action) => {
          localStorage.setItem('accept', 'true')
        }
      })
    }


    if (config.webhost == 'auto') {
      this.weblink = document.domain
    } else {
      this.weblink = config.webhost
    }

    var a = new Date()
    this.hideFeather = config.hideFeather
    this.year = a.getFullYear()
    this.userAgent = navigator.appName + ' ' + navigator.appCodeName + ' ' + navigator.appVersion
    var ak = localStorage.getItem('authkey')
    if (ak) {
      this.$http.post("/api/user/info", {
        authkey: ak
      }).then((res) => {
        if (res.data.data.authkey) {
          this.logon = true
          this.uname = res.data.data.name
          this.$store.commit('login')
          this.$store.commit('name', res.data.data.name)
        } else {
          localStorage.removeItem('authkey')
          this.$store.commit('logout')
          this.$store.commit('name', '')

        }
      })
    }
    useTitle(this.forumName)

    Notification.requestPermission((permission) => { });

    addEventListener("visibilitychange", () => {
      if (document.hidden) {
        useTitle("记得回来哦!")
      } else {
        useTitle(this.forumName)
      }
    });

  },
  methods: {
    changeReload() {
      this.reloadDialog = !this.reloadDialog
    },
    reload() {
      this.changeReload()
      window.location.reload()
    },
    unreload() {
      this.changeReload()
    },

    // login
    submitLogin() {
      if (this.checkName() && this.checkPw()) {
        this.$http.post("/api/user/login", {
          name: this.nm,
          pw: this.pw
        }).then((request) => {
          if (request.data.code == 1011) {
            this.$message.error(request.data.msg)
            this.nm = ""
            this.pw = ""
          } else {
            this.$message.success(request.data.msg)
            localStorage.setItem('authkey', request.data.data.authkey)
            localStorage.setItem('needRef', '/')
            this.$router.push("/")
          }
        }).catch((error) => {
          this.$message.error("登录失败,请检查网络连接!")
        })
      }
    },
    checkNameLogin() {
      if (this.nm == "") {
        this.a = "填写此字段"
        return false
      }
      this.a = ""

      return true
    },
    checkPwLogin() {
      if (this.pw == "") {
        this.b = "填写此字段"
        return false
      }
      this.b = ""

      return true
    }
  },
  // 监听,当路由发生变化的时候执行
}
</script>

<style>
* {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
  /* font-family: 'Nunito', 'Helvetica Neue', Helvetica, Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', sans-serif; */
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


