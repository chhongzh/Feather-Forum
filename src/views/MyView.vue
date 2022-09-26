<template>
    <el-card>
        <template #header>
            <h1>{{ uname }}</h1>
        </template>
        <el-button @click="logout" type="primary">登出</el-button>
    </el-card>
</template>

<script>
export default {
    data() {
        return {
            uname: ''
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
                    localStorage.removeItem('authkey')
                    this.$message.error('未登录');
                    this.$router.push('/')
                }
            })
        } else {
            this.$message.error('未登录');
            this.$store.commit('logout')
            this.$router.push('/')
        }
    },
    methods: {
        logout() {
            window.localStorage.removeItem('authkey')
            this.$message.success('登出成功');
            this.$store.commit('name', '')
            this.$store.commit('logout')
            this.$router.push('/login')
        }
    }
}
</script>

<style>
</style>