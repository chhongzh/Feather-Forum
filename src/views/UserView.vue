<template>
    {{ $route.params.uid }}
    {{ mem.name }}
</template>

<script>
export default {
    data() {
        return {
            mem: {
                name: '',
                coin: 0,
                time: 0
            }
        }
    },
    mounted() {
        if (isNaN(this.$route.params.uid)) {
            this.$message.error('非法用户id');
            this.$router.push('/')
        }
        this.$http.get(`/api/user/info/${this.$route.params.uid}`).then((res) => {
            console.log(res.data.data)
            this.mem.name = res.data.data.name
            this.mem.coin = res.data.data.coin
            this.mem.time = res.data.data.time
        })
    }
}
</script>

<style>
</style>