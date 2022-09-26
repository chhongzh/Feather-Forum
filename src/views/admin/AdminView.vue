<template>
    <el-row>
        <el-col :span="4">
            <el-card>
                欢迎回来:{{ superName }}
            </el-card>
            <el-menu :router="true" :default-active="$route.path">
                <el-menu-item index="/admin/index">仪表盘</el-menu-item>
            </el-menu>
        </el-col>
        <el-col :span="18" :offset="1">
            <router-view />
        </el-col>
    </el-row>
</template>

<script>
export default {
    data() {
        return {
            superName: '',
        }
    },
    mounted() {
        if (!localStorage.getItem('super')) {
            if (this.$route.path != '/admin/login') {
                this.$message.error('未授权登录!');
                this.$router.push('/admin/login')
            }

        }

    }
}
</script>

<style>
</style>