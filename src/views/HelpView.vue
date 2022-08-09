<template>
    <el-row>
        <el-col :span="6">
            <el-menu :default-active="$route.path">
                <el-menu-item @click="defaultView" index="/help">帮助</el-menu-item>
                <el-menu-item @click="privacyView" index="/help/privacy">隐私政策</el-menu-item>
                <el-menu-item @click="cookieView" index="/help/cookie">Cookie的使用</el-menu-item>
                <el-menu-item @click="browserView" index="/help/browser">浏览器</el-menu-item>
            </el-menu>
        </el-col>
        <el-col :span="18">
            <component :is="c"></component>
        </el-col>
    </el-row>
</template>

<script>
import { shallowRef } from 'vue'
import HelpDefault from '@/components/HelpDefault.vue'
import HelpPrivacy from '@/components/HelpPrivacy.vue'
import HelpCookie from '@/components/HelpCookie.vue'
import HelpBrowser from '@/components/HelpBrowser.vue'
export default {
    data() {
        return {
            c: shallowRef(HelpDefault)
        }
    },
    methods: {
        defaultView() {
            this.c = shallowRef(HelpDefault)
        },
        privacyView() {
            this.c = shallowRef(HelpPrivacy)
        },
        cookieView() {
            this.c = shallowRef(HelpCookie)
        },
        browserView() {
            this.c = shallowRef(HelpBrowser)
        }
    }
}
</script>

<style>
</style>