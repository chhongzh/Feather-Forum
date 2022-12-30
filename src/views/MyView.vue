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
                <el-tab-pane label="消息">
                    <div v-if="renderNotification">
                        <p>我们检查到您的浏览器拒绝了消息请求, 因此您可能无法及时收到消息</p>
                        <p>也有可能是因为检测失误, 您可以点击下方按钮进行测试</p>
                        <el-button :disabled="testDisabled" @click="testNotification">{{ test }}</el-button>
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
            renderNotification: true,
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

        if (Notification.permission == "default") {
            this.test = "您还未同意请求"
            this.testDisabled = false
        } else if (Notification.permission == "denied") {
            this.test = "您拒绝了请求"
            this.testDisabled = true
        } else {
            this.test = "您同意了请求"
            this.testDisabled = true
        }
    },
    methods: {
        logout() {
            delLocalAuthkey()
            makeNotification(this.$t('message.hint'), this.$t('message.logoutDone'))
            this.$store.commit('name', '')
            this.$store.commit('logout')
            this.$router.push('/login')
        },
        testNotification() {
            this.test = "测试中..."
            this.testDisabled = true
            Notification.requestPermission((permissions) => {
                if (permissions == "granted") {
                    this.test = "您同意了请求"
                } else if (permissions == "denied") {
                    this.test = "您拒绝了请求"
                } else {
                    this.test = "您还未同意请求"
                    this.testDisabled = false
                }
            })
        }
    }
}
</script>

<style>

</style>