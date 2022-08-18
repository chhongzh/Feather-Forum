<template>

    <!-- <v-md-editor :model-value="postInfo" mode="preview"></v-md-editor> -->
    <el-card shadow="hover">
        <template #header>
            <h1>{{ postTitle }}</h1>
            <p style="color:var(--el-text-color-regular)">
                <font-awesome-icon icon="fa-regular fa-user" />&nbsp;{{ postAuther }}
                &nbsp;&nbsp;
                <font-awesome-icon icon="fa-regular fa-clock" />&nbsp;{{ postTime }}
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
            postInfo: ''
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
        this.$http.post('/api/post/read', {
            authkey: localStorage.getItem('authkey'),
            pid: this.$route.params.pid
        }).then((res) => {
            if (res.data.code = 200) {
                this.postTitle = res.data.data.title
                this.postAuther = res.data.data.name
                this.postContent = res.data.data.content
                this.postTime = res.data.data.time
                this.postTime = transformTime(this.postTime * 1000)

                this.postInfo = "# " + this.postTitle + "\n" + "由 " + this.postAuther + " 发布于 " + this.postTime
            }
        }).catch((res) => {
            console.log(res)
            this.$message.error('网络错误');
            this.$router.push('/')
        })
    },


}
</script>

<style>
.left {
    text-align: right;
}
</style>