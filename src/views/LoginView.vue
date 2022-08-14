<template>
    <div>
        <el-row type="flex" justify="center">
            <el-card header="登录" class="login-box">
                <el-input @blur="checkName()" v-model="nm" size="large" placeholder="用户名"></el-input>
                <p class="alert">{{ a }}</p>
                <div class="space"></div>
                <el-input @blur="checkPw()" type="password" v-model="pw" size="large" clearable show-password
                    placeholder="密码">
                </el-input>
                <p class="alert">{{ b }}</p>
                <div class="space"></div>
                <el-button type="primary" @click="submit()" size="large">提交</el-button>
                <div class="space"></div>
                <router-link to="/register">
                    <el-link>没有账号?点我注册!</el-link>
                </router-link>
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
            pw: "",
            nm: ""
        }
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
                        this.$router.push("/")
                    }
                }).catch((error) => {
                    this.$message.error("登录失败,请检查网络连接!")
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
        }
    }
}
</script>

<style scoped>
.space {
    margin-top: 24px;
}
</style>