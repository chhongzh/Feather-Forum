<template>
    <el-row type="flex" justify="center">
        <el-card style="width:80%">
            <template #header>
                <h1>{{ uname }}</h1>
            </template>
            <el-tabs tab-position="left" style="" class="demo-tabs">
                <el-tab-pane label="常规">
                    <el-button @click="logout" type="primary">{{ $t('message.logout') }}</el-button>
                </el-tab-pane>
                <el-tab-pane label="账户">Config</el-tab-pane>
                <el-tab-pane label="通知">
                    <div v-show="renderNotification">
                        <p>我们检查到您的浏览器拒绝了通知权限, 因此您可能无法及时收到消息</p>
                        <p>若要打开, 请前往设置中打开本网站"通知"权限</p>
                    </div>
                    <div v-show="!renderNotification">
                        <p>您可以接收本网站的通知, 一切都是正常的</p>
                    </div>
                </el-tab-pane>
                <el-tab-pane label="更多"></el-tab-pane>
            </el-tabs>
        </el-card>
    </el-row>
</template>

<script>
import { makeNotification } from '@/lib/utils'
import { delLocalAuthkey } from '@/lib/auth'

export default {
    data() {
        return {
            uname: '',
            renderNotification: false,
            test: "测试",
            testDisabled: false
        }
    },
    mounted() {
        var ak = localStorage.getItem('authkey')
        if (ak) {
            this.$http.post("/api/user/info", {
                authkey: ak
            }).then((res) => {
                if (res.data.data.authkey) {
                    this.uname = res.data.data.name
                } else {
                    delLocalAuthkey()
                    makeNotification(this.$t('message.hint'), this.$t('message.notLogin'))
                    this.$router.push('/')
                }
            })
        } else {
            makeNotification(this.$t('message.hint'), this.$t('message.notLogin'))
            this.$store.commit('logout')
            this.$router.push('/')
        }

        if (Notification.permission != "granted") {
            this.renderNotification = true
        }
    },
    methods: {
        logout() {
            delLocalAuthkey()
            makeNotification(this.$t('message.hint'), this.$t('message.logoutDone'))
            this.$store.commit('name', '')
            this.$store.commit('logout')
            this.$router.push('/login')
        }
    }
}
</script>

<style>

</style>