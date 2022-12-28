<template>
    <el-card>
        <template #header><b>{{ $t('message.postList') }}</b></template>
        <el-empty v-show="posts.length <= 0" :description="$t('message.noData')">

        </el-empty>
        <div v-for="(pst, index) in posts" :key="index">
            <el-card>
                <template #header>
                    <router-link :to="`/post/${pst.pid}`">
                        <el-link>{{ pst.title }}</el-link>
                    </router-link>
                </template>
                {{ pst.content }}
                <el-divider></el-divider>
                {{ $t('message.user') }}:
                <router-link :to="`/user/${pst.uid}`">
                    <el-link>{{ pst.name }}</el-link>
                </router-link>
                {{ $t('message.sendin') }}:{{ trans(pst.time * 1000) }}
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
        },
        trans(a) {
            return transformTime(a)
        }
    }

}
</script>

<style>

</style>