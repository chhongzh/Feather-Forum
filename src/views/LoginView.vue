<template>
    <div>
        <el-row type="flex" justify="center">
            <el-card :header="$t('message.login')" class="login-box">
                <el-input @blur="checkName()" v-model="nm" size="large"
                    :placeholder="$t('message.username')"></el-input>
                <p class="alert">{{ nameMessage }}</p>
                <div class="space"></div>
                <el-input @blur="checkPw()" type="password" v-model="pw" size="large" clearable show-password
                    :placeholder="$t('message.password')">
                </el-input>
                <p class="alert">{{ passwordMessage }}</p>
                <div class="space"></div>
                <el-button type="primary" @click="submit()" size="large">{{ $t('message.submit') }}</el-button>
                <div class="space"></div>
                <router-link to="/register">
                    <el-link>{{ $t('message.noAccount') }}</el-link>
                </router-link>
            </el-card>
        </el-row>
    </div>
</template>

<script>
import { validateAuthkey, getLocalAuthkey } from '@/lib/auth'

export default {
    data() {
        return {
            nameMessage: "",
            passwordMessage: "",
            pw: "",
            nm: ""
        }
    },
    mounted() {
        var ak = getLocalAuthkey();
        if (ak) {
            validateAuthkey(ak).then((res) => {
                if (res.data.authkey) {
                    this.$message.error(this.$t('message.logged'))
                    this.$router.push('/')
                }
            })
        }
    },
    methods: {
        submit() {
            if (this.checkName() && this.checkPw()) {
                this.$http.post("/api/user/login", {
                    name: this.nm,
                    pw: this.pw
                }).then((request) => {
                    if (request.data.code == 1011) {
                        this.$message.error(request.data.msg)
                        this.nm = ""
                        this.pw = ""
                    } else {
                        this.$message.success(request.data.msg)
                        localStorage.setItem('authkey', request.data.data.authkey)
                        this.$store.commit('login')
                        this.$store.commit('name', this.nm)
                        this.$router.push("/")
                    }
                }).catch((error) => {
                    this.$message.error(this.$t("message.loginError"))
                })
            }
        },
        checkName() {
            if (this.nm == "") {
                this.nameMessage = this.$t('message.fillThis')
                return false
            }
            this.nameMessage = ""

            return true
        },
        checkPw() {
            if (this.pw == "") {
                this.passwordMessage = this.$t('message.fillThis')
                return false
            }
            this.passwordMessage = ""

            return true
        }
    }
}
</script>

<style scoped>
.space {
    margin-top: 24px;
}
</style>