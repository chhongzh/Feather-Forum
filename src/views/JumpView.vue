<template>
    <el-row type="flex" justify="center">
        <el-card header="跳转提示" style="width:80%">
            <p><b>{{$route.query.url}}</b>不属于{{forum}},继续前往?</p>
            <div style="text-align: right;">
                <el-button @click="f">继续前往</el-button>
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
    methods: {
        f() {
            window.location.href = this.$route.query.url
        }
    }
}
</script>