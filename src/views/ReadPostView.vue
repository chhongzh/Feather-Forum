<template>
    <el-card shadow="hover">
        <template #header>
            <h1>{{ postTitle }}</h1>
            <p style="color:var(--el-text-color-regular)">
            </p>
        </template>
        <v-md-editor :model-value="postContent" mode="preview"></v-md-editor>
    </el-card>
</template>

<script>
import { transformTime } from '../assets/js/date.js'
export default {
    data() {
        return {
            postTitle: '',
            postAuther: '',
            postTime: '',
            postContent: '',
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
        console.log(window.sessionStorage.getItem('cacheOBJpid'))
        if (window.sessionStorage.getItem('cacheOBJpid') == this.$route.params.pid) {
            this.postTitle = window.sessionStorage.getItem('cacheOBJtitle')
            this.postAuther = window.sessionStorage.getItem('cacheOBJauther')
            this.postContent = window.sessionStorage.getItem('cacheOBJcontent')
            this.postTime = window.sessionStorage.getItem('cacheOBJtime')
        } else {
            this.$http.post('/api/post/read', {
                authkey: localStorage.getItem('authkey'),
                pid: this.$route.params.pid
            }).then((res) => {
                if (res.data.code = 200) {
                    window.sessionStorage.setItem('cacheOBJpid', this.$route.params.pid)
                    window.sessionStorage.setItem('cacheOBJtitle', res.data.data.title)
                    window.sessionStorage.setItem('cacheOBJauther', res.data.data.name)
                    window.sessionStorage.setItem('cacheOBJcontent', res.data.data.content)
                    window.sessionStorage.setItem('cacheOBJtime', transformTime(res.data.data.time * 1000))

                    console.log(1)
                    this.postTitle = res.data.data.title
                    this.postAuther = res.data.data.nam
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


}
</script>

<style>
.left {
    text-align: right;
}
</style>