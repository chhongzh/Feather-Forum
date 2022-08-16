<template>
    <el-row type="flex" justify="center">
        <el-card header="管理员登录" shadow="hover" class="login-box">
            <el-input size="large" v-model="n" placeholder="Username" clearable></el-input>
            <div class="b"></div>
            <el-input size="large" v-model="p" placeholder="Password" clearable></el-input>
            <div class="b"></div>
            <el-button size="large" type="primary">登录</el-button>
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
    }
}
</script>

<style scoped>
.b {
    margin-top: 20px;
}
</style>
