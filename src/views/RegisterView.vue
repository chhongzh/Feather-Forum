<template>
    <div>
        <el-row type="flex" justify="center">
            <el-card class="login-box" :header="$t('message.register')">
                <el-input @blur="checkName()" v-model="nm" clearable size="large"
                    :placeholder="$t('message.username')"></el-input>
                <p class="alert">{{ a }}</p>
                <div class="space"></div>
                <el-input @blur="checkPw()" type="password" v-model="pw" size="large" clearable show-password
                    :placeholder="$t('message.password')">
                </el-input>
                <p class="alert">{{ b }}</p>
                <div class="space"></div>
                <el-input @blur="checkPw1()" type="password" v-model="pw1" size="large" clearable show-password
                    :placeholder="$t('message.checkPassword')">
                </el-input>
                <p class="alert">{{ c }}</p>
                <div class="space"></div>
                <el-input @blur="checkEmail()" type="email" v-model="email" size="large" clearable
                    :placeholder="$t('message.email')">
                </el-input>
                <p class="alert">{{ d }}</p>
                <div class="space"></div>
                <el-button type="primary" :loading="loading" @click="submit()" size="large">{{ $t('message.submit')
                    }}</el-button>
            </el-card>
        </el-row>
    </div>
</template>

<script>
export default {
    data() {
        return {
            a: "",
            b: "",
            c: "",
            d: "",
            pw: "",
            pw1: "",
            email: "",
            nm: "",
            loading: false // 多次提交 防抖 issues#3
        }
    },
    methods: {
        submit() {
            if (this.checkName() && this.checkPw() && this.checkEmail() && this.checkPw1()) {
                this.loading = true
                this.$http.post("/api/user/register", {
                    name: this.nm,
                    pw: this.pw,
                    email: this.email
                }).then((request) => {
                    if (request.data.code != 200) {
                        this.$message.error(request.data.msg)
                        this.nm = ""
                        this.pw = ""
                        this.pw1 = ""
                        this.email = ""
                        this.loading = false
                    } else {
                        this.$message.success(request.data.msg)
                        this.$router.push("/login")
                        this.loading = false
                    }
                }).catch((error) => {
                    this.loading = false
                    console.log(error)
                })
            }
        },
        checkName() {
            if (this.nm == "") {
                this.a = this.$t('message.fillThis')
                return false
            }
            this.a = ""

            return true
        },
        checkPw() {
            if (this.pw == "") {
                this.b = this.$t('message.fillThis')
                return false
            }
            this.b = ""

            return true
        },
        checkPw1() {
            if (this.pw == "") {
                this.c = this.$t('message.fillThis')
                return false
            }
            if (this.pw != this.pw1) {
                this.c = this.$t('message.notValidate')
                return false
            }
            this.c = ""

            return true
        }, checkEmail() {
            if (this.email == "") {
                this.d = this.$t('message.fillThis')
                return false
            }
            this.d = ""

            return true
        },
    },
    mounted() {
        var ak = localStorage.getItem('authkey')
        if (ak) {
            this.$http.post("/api/authkey/v", {
                authkey: ak
            }).then((res) => {
                if (res.data.data.authkey) {
                    this.$message.error(this.$t('message.logged'))
                    this.$router.push("/")
                }
            })
        }
    }
}
</script>

<style scoped>
.space {
    margin-top: 24px;
}
</style>