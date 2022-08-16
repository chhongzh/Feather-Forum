<template>
    <el-card header="用户列表">
        <el-card :header="mem.name" v-for="mem in mems" :key="mem.name">
            <el-descriptions>
                <el-descriptions-item label="用户名">{{ mem.name }}</el-descriptions-item>
                <el-descriptions-item label="金币">{{ mem.coin }}</el-descriptions-item>
                <el-descriptions-item label="Place"></el-descriptions-item>
                <el-descriptions-item label="Remarks">
                    <el-tag size="small">School</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="Address">No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu
                    Province</el-descriptions-item>
            </el-descriptions>
        </el-card>
        <el-row type="flex" justify="center">
            <el-button @click="load" type="primary">加载更多...</el-button>
        </el-row>
    </el-card>




</template>

<script>
export default {
    data() {
        return {
            count: 0,
            mems: [],
            last: false,
            page: 0,
            height: 500
        }
    },
    mounted() {
        this.load()
    },
    methods: {
        load() {
            this.getApi()
            this.count += 1
        },
        getApi() {
            if (!this.last) {
                this.$http.get(`/api/user/list?page=${this.count}`)
                    .then((res) => {
                        // this.mems = (res.data.data.list)
                        this.mems = this.mems.concat(res.data.data.list)
                        this.last = res.data.data.last
                    }).catch((res) => {
                        console.log(res)
                    })
            }

        }

    }

}
</script>

<style>
</style>