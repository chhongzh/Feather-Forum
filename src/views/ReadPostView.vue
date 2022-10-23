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
                        <el-input v-model="input1" placeholder="Please input">
                            <template #prepend>Http://</template>
                        </el-input>
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
        if ((this.$store.state.post.pid != 0) && this.$store.state.post.pid == this.$route.params.pid) {
            this.postTitle = this.$store.state.post.title
            this.postAuther = this.$store.state.post.auth
            this.postContent = this.$store.state.post.content
            this.postTime = this.$store.state.post.time
            this.postUid = this.$store.state.post.uid
        } else {
            this.$http.post('/api/post/read', {
                authkey: localStorage.getItem('authkey'),
                pid: this.$route.params.pid
            }).then((res) => {
                if (res.data.code = 200) {
                    this.$store.commit('setpost', {
                        pid: this.$route.params.pid,
                        content: res.data.data.content,
                        title: res.data.data.title,
                        auth: res.data.data.name,
                        time: res.data.data.time,
                        uid: res.data.data.uid,
                    })
                    // console.log(this.$store.state)
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