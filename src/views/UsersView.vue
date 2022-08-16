<template>
    <el-card header="用户列表">
        <el-empty v-show="mems.length <= 0" description="没有数据">

        </el-empty>
        <el-card v-for="(mem, index) in mems" :key="index">
            <template #header>
                {{ mem.name }}
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
        <el-row type="flex" justify="center">
            <el-pagination :page-count="totalPage" @current-change="onChange" :hide-on-single-page="true"
                v-model:current-page="page" layout="prev, pager, next, jumper">
            </el-pagination>
        </el-row>
    </el-card>
</template>

<script>
export default {
    data() {
        return {
            totalPage: 1,
            page: 1,
            cache: 0,
            mems: []
        }
    },
    mounted() {
        this.$http.get('/api/user/page').then((res) => {
            this.totalPage = res.data.data.page + 1
        })
        this.onChange()
    },
    methods: {
        onChange() {
            this.$http(`/api/user/list?page=${this.page - 1}`).then((res) => {
                this.mems = res.data.data.list
                console.log(this.mems)
            }).catch((res) => {
                this.$message.error(res);
            })
        }
    }

}
</script>

<style>
</style>