<template>
    <el-container>
        <el-aside width="200px">
            <el-affix>
                <el-menu :default-active="$route.fullPath" :router="true">
                    <el-menu-item index="/admin">主页</el-menu-item>
                    <el-menu-item index="/admin/logs">日志</el-menu-item>
                </el-menu>
            </el-affix>
        </el-aside>
        <el-container>
            <el-header>
                <el-page-header @back="$router.back()" v-show="$route.meta.showPageHeader">
                    <template #content>
                        <b>{{$route.meta.title}}</b>
                    </template>
                </el-page-header>
                <div v-show="!$route.meta.showPageHeader">
                    <h1>{{$route.meta.title}}</h1>
                </div>
            </el-header>
            <el-main>
                <!-- Start router -->
                <router-view />
                <!-- End router -->
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
    beforeRouteUpdate() {
        if (new Date().getTime() > (this.$store.state.admin.last + 3600) * 1000) {
            this.$message.error('登录过期,请重试')
            this.$store.commit('admin', false)
            this.$router.push('/admin/login')
        }
    }
}
</script>