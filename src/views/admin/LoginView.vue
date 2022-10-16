<template>
    <el-row type="flex" justify="center">
        <el-card header="管理员登录" shadow="hover" class="login-box">
            <el-input size="large" v-model="n" placeholder="Username" type="text" clearable></el-input>
            <div class="b"></div>
            <el-input size="large" v-model="p" placeholder="Password" type="password" clearable></el-input>
            <div class="b"></div>
            <el-button size="large" @click="login" :loading="lockstate.login" type="primary">登录</el-button>
        </el-card>
    </el-row>

</template>

<script>
export default {
    data() {
        return {
            n: '',
            p: '',
            lockstate: {
                login: false
            }
        }
    },
    mounted() {
        if (this.$store.state.admin.login) {
            this.$message.success('鉴权成功');
            this.$router.push('/admin')
        }
    },
    methods: {
        login() {
            this.lockstate.login = true
            this.$http.post('/api/admin/login', { name: this.n, pw: this.p }).then((res) => {
                res = res.data
                if (res.code == 200) {
                    this.$message.success('鉴权成功');
                    this.$store.commit('admin', true, res.data.authkey)
                    this.$router.push('/admin')
                    this.lockstate.login = false
                } else {
                    this.$message.error(res.msg)
                    this.lockstate.login = false
                }
            })
        }
    }
}
</script>
    

<style>

</style>