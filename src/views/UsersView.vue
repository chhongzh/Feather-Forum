<template>
    <el-card v-loading="isLoading">
        <template #header><b>用户列表</b></template>
        <el-empty v-show="mems.length <= 0" description="没有数据">

        </el-empty>
        <div v-for="(mem, index) in mems" :key="index">
            <el-card>
                <template #header>
                    <router-link :to="`/user/${mem.uid}`">
                        <el-link>{{ mem.name }}</el-link>
                    </router-link>
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
            <div class="foot-space"></div>
        </div>
        <el-row type="flex" justify="center">
            <el-pagination :page-count="totalPage" @current-change="onChange" :hide-on-single-page="true"
                v-model:current-page="page" layout="prev, pager, next, jumper">
            </el-pagination>
        </el-row>
    </el-card>
</template>

<script>
import { transformTime } from '@/assets/js/date.js'

export default {
    data() {
        return {
            totalPage: 1,
            page: 1,
            cache: 0,
            mems: [],
            isLoading: true
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
            this.isLoading = true
            this.$http(`/api/user/list?page=${this.page - 1}`).then((res) => {
                // this.mems = res.data.data.list
                this.mems = []
                for (var i = 0; i < res.data.data.list.length; i++) {
                    res.data.data.list[i].time = transformTime(res.data.data.list[i].time * 1000)
                    this.mems.push(res.data.data.list[i])
                }
            })
                .catch((res) => {
                    this.$message.error(res);
                })
            this.isLoading = false
        }
    }

}
</script>

<style>

</style>