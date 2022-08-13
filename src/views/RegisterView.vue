<template>
    <div>
        <el-input @blur="checkName()" v-model="nm" clearable size="large" placeholder="用户名"></el-input>
        <p class="alert">{{ a }}</p>
        <div class="space"></div>
        <el-input @blur="checkPw()" type="password" v-model="pw" size="large" clearable show-password placeholder="密码">
        </el-input>
        <p class="alert">{{ b }}</p>
        <div class="space"></div>
        <el-input @blur="checkPw1()" type="password" v-model="pw1" size="large" clearable show-password
            placeholder="确认密码">
        </el-input>
        <p class="alert">{{ c }}</p>
        <div class="space"></div>
        <el-input @blur="checkEmail()" type="email" v-model="email" size="large" clearable placeholder="邮箱">
        </el-input>
        <p class="alert">{{ d }}</p>
        <div class="space"></div>
        <el-button type="primary" @click="submit()" size="large">提交</el-button>
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
            nm: ""
        }
    },
    methods: {
        submit() {
            if (this.checkName() && this.checkPw() && this.checkEmail() && this.checkPw1()) {
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
                    } else {
                        this.$message.success(request.data.msg)
                        // new Notification("你好世界", { body: "你好" })
                        this.$router.push("/login")

                    }
                }).catch((error) => {
                    console.log(error)
                })
            }
        },
        checkName() {
            if (this.nm == "") {
                this.a = "填写此字段"
                return false
            }
            this.a = ""

            return true
        },
        checkPw() {
            if (this.pw == "") {
                this.b = "填写此字段"
                return false
            }
            this.b = ""

            return true
        },
        checkPw1() {
            if (this.pw == "") {
                this.c = "填写此字段"
                return false
            }
            if (this.pw != this.pw1) {
                this.c = "无法验证您的密码,请重试"
                return false
            }
            this.c = ""

            return true
        }, checkEmail() {
            if (this.email == "") {
                this.d = "填写此字段"
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
                    this.$message.error("你已经登录过啦!")
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