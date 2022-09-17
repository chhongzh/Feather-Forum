<template>
    <el-card>
        <template #header><b>帖子列表</b></template>
        <el-empty v-show="posts.length <= 0" description="没有数据">

        </el-empty>
        <div v-for="(pst, index) in posts" :key="index">
            <el-card>
                <template #header>
                    <router-link :to="`/post/${pst.uid}`">
                        <el-link>{{ pst.title }}</el-link>
                    </router-link>
                </template>
                {{pst}}
                <!-- <el-descriptions>
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

                </el-descriptions> -->
                <el-divider></el-divider>
                {{pst.uid}}
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
            posts: []
        }
    },
    mounted() {
        this.$http.get('/api/post/page').then((res) => {
            this.totalPage = res.data.data.page + 1
        })
        this.onChange()
    },
    methods: {
        onChange() {
            this.$http(`/api/post/list?page=${this.page - 1}`).then((res) => {
                this.posts = res.data.data.list
            })
                .catch((res) => {
                    this.$message.error(res);
                })
        }
    }

}
</script>

<style>

</style>