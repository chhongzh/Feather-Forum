<template>
    <el-card>
        <template #header>
            <b>{{ mem.name }}</b> 的主页
        </template>

        <el-descriptions>
            <el-descriptions-item label="个性签名">
                {{ mem.avartar }}
            </el-descriptions-item>
            <el-descriptions-item label="UID">
                {{ mem.uid }}
            </el-descriptions-item>
            <el-descriptions-item label="金币">
                {{ mem.coin }}
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">
                {{ mem.time }}
            </el-descriptions-item>
        </el-descriptions>
    </el-card>
</template>

<script>
import { transformTime } from '@/assets/js/date';
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
        console.log()
        if (isNaN(this.$route.params.uid) || Number(this.$route.params.uid) <= 0) {
            this.$message.error(isNaN(this.$route.params.uid) ? '用户id应为数字' : '用户id应大于等于0');
            this.$router.push('/user')
        } else {
            this.$http.get(`/api/user/info/${this.$route.params.uid}`).then((res) => {
                console.log(res.data)
                if (res.data.code == 1020) {
                    this.$message.error(res.data.msg)
                    this.$router.push('/user')
                } else {
                    this.mem.name = res.data.data.name
                    this.mem.coin = res.data.data.coin
                    this.mem.time = res.data.data.time
                    this.mem.time = transformTime(res.data.data.time * 1000)
                    this.mem.uid = res.data.data.uid
                    this.mem.avartar = res.data.data.avartar
                }
            })
        }
    }
}
</script>

<style>
</style>