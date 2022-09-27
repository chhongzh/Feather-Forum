<template>
    <el-row type="flex" justify="center">
        <el-card header="跳转提示" style="width:80%">
            <p><b>{{$route.query.url}}</b>不属于{{forum}},继续前往?</p>
            <div style="text-align: right;">
                <el-button @click="b">返回</el-button>
                <el-button @click="f">在新标签页打开并返回</el-button>
            </div>
        </el-card>
    </el-row>
</template>

<script>
import config from '@/assets/js/config';
export default {
    data() {
        return {
            forum: config.forumName
        }
    },
    mounted() {
        if ((!this.$route.query.path) || (!this.$route.query.url)) {
            this.$message.error('参数缺失');
            this.$router.push('/')
        }
    },
    methods: {
        f() {
            window.open(this.$route.query.url, "_blank")
            this.$router.push(this.$route.query.path)
        },
        b() {
            this.$router.push(this.$route.query.path)
        }
    }
}
</script>