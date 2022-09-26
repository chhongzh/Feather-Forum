<template>
    <el-card>
        <div>
            <p>此页面将会介绍可以用于访问本页面的浏览器。</p>
            <h3>推荐使用的浏览器</h3>
            <p>我们<b>推荐</b>您使用一下的浏览器,因为其可以正常浏览<b>{{ website }}</b></p>
            <ul>
                <li>Google Chrome</li>
                <li>Mozilla Firefox</li>
                <li>Microsoft Edge</li>
            </ul>
        </div>
    </el-card>
</template>

<script>
import config from '../assets/js/config.js'
export default {
    data() {
        return {
            website: ''
        }
    },
    mounted() {
        this.website = config.forumName
    }
}
</script>

<style>
</style>