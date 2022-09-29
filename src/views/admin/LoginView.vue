<template>
    <el-row type="flex" justify="center">
        <el-card header="管理员登录" shadow="hover" class="login-box">
            <el-input size="large" v-model="n" placeholder="Username" type="text" clearable></el-input>
            <div class="b"></div>
            <el-input size="large" v-model="p" placeholder="Password" type="password" clearable></el-input>
            <div class="b"></div>
            <el-button size="large" @click="login" type="primary">登录</el-button>
        </el-card>
    </el-row>

</template>

<script>
export default {
    data() {
        return {
            n: '',
            p: ''
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
            this.$http.post('/api/admin/login', { name: this.n, pw: this.p }).then((res) => {
                res = res.data
                if (res.code == 200) {
                    this.$message.success('鉴权成功');
                    this.$store.commit('admin', true, res.data.authkey)
                    this.$router.push('/admin')
                } else {
                    this.$message.error(res.msg)
                }
            })
        }
    }
}
</script>
    

<style>

</style>