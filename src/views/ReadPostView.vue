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
                            {{ postAuther }}
                        </router-link>
                    </b>
                    ·
                    <el-icon>
                        <Calendar />
                    </el-icon>
                    <b>{{ postTime }}</b>
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
import { validateAuthkey, getLocalAuthkey, delLocalAuthkey } from '@/lib/auth'
import { makeNotification } from '@/lib/utils'
import { transformTime } from '../assets/js/date.js'
import { getPost } from '@/lib/post'
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
        var ak = getLocalAuthkey()
        if (!ak) {
            validateAuthkey(ak).then((res) => {
                if (!res.data.authkey) {
                    makeNotification("", this.$t('message.loginFail'))
                    delLocalAuthkey()
                    this.$router.push("/login")
                }
            })
        }
        if (isNaN(this.$route.params.pid)) {
            makeNotification('', this.$t('message.postNan'))
            this.$router.push('/')
        }
        if ((this.$store.state.post.pid != 0) && this.$store.state.post.pid == this.$route.params.pid) {
            this.postTitle = this.$store.state.post.title
            this.postAuther = this.$store.state.post.auth
            this.postContent = this.$store.state.post.content
            this.postTime = transformTime(this.$store.state.post.time * 1000) // 修复 issues #5
            this.postUid = this.$store.state.post.uid
        } else {
            getPost(this.$route.params.pid, ak).then((res) => {
                this.$store.commit('setpost', {
                    pid: this.$route.params.pid,
                    content: res.data.content,
                    title: res.data.title,
                    auth: res.data.name,
                    time: res.data.time,
                    uid: res.data.uid,
                })
                this.postTitle = res.data.title
                this.postAuther = res.data.name
                this.postContent = res.data.content
                this.postTime = res.data.time
                this.postTime = transformTime(this.postTime * 1000)
            }).catch((res) => {
                makeNotification('', this.$t('message.networkError'))
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
            makeNotification('', this.$t('message.copied'))
        }
    }
}
</script>

<style>
.left {
    text-align: right;
}
</style>