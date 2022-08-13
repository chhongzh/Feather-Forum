<template>
  <!-- <el-row> -->
  <!-- <el-col :span="3"></el-col> -->
  <!-- <el-col :span="18"> -->


  <el-container>
    <el-affix>
      <el-header>
        <el-menu mode="horizontal" :ellipsis="false" :router="true" :default-active="$route.path">
          <el-menu-item index="/" style="font-size:14px">{{ forumName }}</el-menu-item>
          <el-sub-menu index="帖子">
            <template #title>帖子</template>


            <el-menu-item index="/post/write">发布</el-menu-item>

          </el-sub-menu>
          <div class="flex-grow"></div>

          <el-switch class="top" inline-prompt :inactive-icon="Moon" :active-icon="Sunny" v-model="switchModel"
            @click="toggleDark()"></el-switch>
          <div class="left-space"></div>

          <el-menu-item v-if="!logon" index="/login">
            <el-space :size="5">
              <font-awesome-icon icon="fa-regular fa-circle-user" />
              登录
            </el-space>
          </el-menu-item>
          <el-menu-item v-if="!logon" index="/register">
            <el-space :size="5">
              <font-awesome-icon icon="fa-regular fa-clipboard" />
              注册
            </el-space>
          </el-menu-item>
          <el-menu-item v-if="logon" index="/my">{{ uname }}</el-menu-item>
        </el-menu>
      </el-header>
    </el-affix>
    <el-main>
      <!-- <h1 class="title">{{ $route.name }}</h1> -->
      <div class="foot-space"></div>
      <div v-show="!logon">
        <el-card>
          <div>
            <p>访客,请先登录</p>
          </div>
        </el-card>
        <div class="foot-space"></div>

      </div>
      <el-scrollbar>
        <router-view :key="$route.fullPath" />
      </el-scrollbar>
    </el-main>
    <el-divider />
    <el-footer class="little">
      <div class="foot-space"></div>

      <b>{{ userAgent }}</b>
      <el-row>
        <el-col :span="8">
          <!-- <p v-if="!hideFeather"><b>"{{ forumName }}"</b> 由 "<b>Feather Forum</b>" 提供支持</p> -->
          <p v-if="!hideFeather">"<b>{{ forumName }}</b>" 由 "<b>
              <el-link :underline="false" href="https://github.com/chhongzh/Feather-Forum">Feather Forum
              </el-link>
            </b>" 提供支持</p>
          <p>Client响应:<b>{{ clientTime }}</b></p>
          <p v-if="logon">Server响应:<b>{{ serverTime }}</b></p>
          <p v-if="logon">响应时间:<b>{{ reduceTime }}</b></p>
        </el-col>
        <el-col :span="8">
          <p>
            © Copyright {{ year }} {{ weblink }} All Rights Reserved
          </p>
          <p>
            © {{ year }} {{ weblink }} 版权所有
          </p>

        </el-col>
        <el-col :span="8">
          <p><b>版权所有 侵权必究!</b></p>
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
  <!-- </el-col> -->
  <!-- <el-col :span="3"> -->
  <div>
  </div>
  <!-- </el-col> -->
  <!-- </el-row> -->

  <!-- Begain Dialog -->
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
import { Sunny, Moon, User } from '@element-plus/icons-vue'
import { useDark, useToggle, useTitle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)
</script>

<script>
import config from './assets/js/config.js'
export default {
  components: { Sunny, Moon, User },
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
      clientTime: '请先登录',
      serverTime: '请先登录',
      reduceTime: '请先登录',
      reloadDialog: false
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
    this.clientTime = a.getTime() / 1000
    this.userAgent = navigator.appName + ' ' + navigator.appCodeName + ' ' + navigator.appVersion
    var ak = localStorage.getItem('authkey')
    if (ak) {
      this.$http.post("/api/user/info", {
        authkey: ak
      }).then((res) => {
        if (res.data.data.authkey) {
          this.logon = true
          this.uname = res.data.data.name
          this.serverTime = res.data.time
          this.reduceTime = (this.serverTime - this.clientTime).toFixed(3)
        } else {
          localStorage.removeItem('authkey')
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
    }
  }
}
</script>

<style>
@import url("./assets/fonts/fonts.css");

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
</style>


