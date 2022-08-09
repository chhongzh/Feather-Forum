<template>
    <div>
        <h1>重新加载</h1>
        <p>当页面出现一下问题时,你可以尝试重新加载页面</p>
        <el-button-group>
            <el-button @click="restart" type="primary">重新加载</el-button>
            <el-button @click="goBack" type="info">返回</el-button>
        </el-button-group>
    </div>
</template>

<script>
export default {
    methods: {
        goBack() {
            this.$router.push('/')
        },
        restart() {
            this.$router.push('/')
            window.location.reload()
        }
    }
}
</script>

<style>
</style>