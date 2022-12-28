<template>
    <el-row type="flex" justify="center">
        <el-card :header="$t('message.jumpTip')" style="width:80%">
            <p><b>{{ $route.query.url }}</b>{{ $t('message.notBelong') + forum + ',' + $t('message.continueTo') + '?' }}
            </p>
            <div style="text-align: right;">
                <el-button @click="b">{{ $t('message.back') }}</el-button>
                <el-button @click="f">{{ $t('message.newBlankAndBack') }}</el-button>
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
        if ((!this.$route.query.redirect) || (!this.$route.query.url)) {
            this.$message.error(this.$t('message.missingArg'));
            this.$router.push('/')
        }
    },
    methods: {
        f() {
            window.open(this.$route.query.url, "_blank")
            this.$router.push(this.$route.query.redirect)
        },
        b() {
            this.$router.push(this.$route.query.redirect)
        }
    }
}
</script>