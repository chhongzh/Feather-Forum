<template>
    <el-card shadow="hover">
        <template #header>
            <h1>{{ postTitle }}</h1>
            <el-row justify="space-between">
                <div>
                    <el-icon>
                        <User />
                    </el-icon>
                    <b>
                        <router-link style="color:var(--el-text-color-primary)" :to="`/user/${postUid}`">
                            {{postAuther}}
                        </router-link>
                    </b>
                    ·
                    <el-icon>
                        <Calendar />
                    </el-icon>
                    <b>{{postTime}}</b>
                </div>
                <el-popover title="分享" placement="top">
                    <template #reference>
                        <el-icon>
                            <Share />
                        </el-icon>
                    </template>
                    <el-button-group>
                        <el-button @click="shareWithMail">邮箱</el-button>
                        <el-button @click="shareWithLink">链接</el-button>
                    </el-button-group>
                </el-popover>
            </el-row>
        </template>
        <v-md-editor :model-value="postContent" mode="preview"></v-md-editor>
    </el-card>
</template>

<script setup>
import { useClipboard } from '@vueuse/core'
const { text, copy, copied, isSupported } = useClipboard(document.URL)
</script>

<script>
import { User, Calendar, Share } from '@element-plus/icons-vue'
import { transformTime } from '../assets/js/date.js'
import config from '@/assets/js/config'
export default {
    components: { User, Calendar, Share },
    data() {
        return {
            postTitle: '',
            postAuther: '',
            postTime: '',
            postContent: '',
            postUid: '',
        }
    },
    mounted() {
        var ak = localStorage.getItem('authkey')
        if (!ak) {
            this.$http.post("/api/authkey/v", {
                authkey: ak
            }).then((res) => {
                if (!res.data.data.authkey) {
                    this.$message.error('未登录或登录过期,请重新登陆');
                    localStorage.removeItem('authkey')
                    this.$router.push("/login")
                }

            })

        }
        if (isNaN(this.$route.params.pid)) {
            this.$message.error('非法帖子id');
            this.$router.push('/')
        }
        if (typeof (window.localStorage.getItem('cacheOBJpid')) != undefined && window.localStorage.getItem('cacheOBJpid') == this.$route.params.pid) {
            this.postTitle = window.localStorage.getItem('cacheOBJtitle')
            this.postAuther = window.localStorage.getItem('cacheOBJauther')
            this.postContent = window.localStorage.getItem('cacheOBJcontent')
            this.postTime = window.localStorage.getItem('cacheOBJtime')
            this.postUid = window.localStorage.getItem('cacheOBJuid')
        } else {
            this.$http.post('/api/post/read', {
                authkey: localStorage.getItem('authkey'),
                pid: this.$route.params.pid
            }).then((res) => {
                if (res.data.code = 200) {
                    window.localStorage.setItem('cacheOBJpid', this.$route.params.pid)
                    window.localStorage.setItem('cacheOBJtitle', res.data.data.title)
                    window.localStorage.setItem('cacheOBJauther', res.data.data.name)
                    window.localStorage.setItem('cacheOBJcontent', res.data.data.content)
                    window.localStorage.setItem('cacheOBJtime', transformTime(res.data.data.time * 1000))
                    window.localStorage.setItem('cacheOBJuid', res.data.data.uid)
                    this.postTitle = res.data.data.title
                    this.postAuther = res.data.data.name
                    this.postContent = res.data.data.content
                    this.postTime = res.data.data.time
                    this.postTime = transformTime(this.postTime * 1000)
                }
            }).catch((res) => {
                this.$message.error('网络错误');
                this.$router.push('/')
            })
        }
    },
    methods: {
        shareWithMail() {
            var body = `我在${config.forumName}看到了由${this.postAuther}发布的文章。\n链接:${document.URL}`
            var title = `文章分享:${this.postTitle}`
            var template = encodeURI(`mailto:?subject=${title}&body=${body}`)
            window.open(template, '_blank')
        },
        shareWithLink() {
            this.copy(document.URL)
            this.$message.success('链接已经复制!')
        }
    }
}
</script>

<style>
.left {
    text-align: right;
}
</style>