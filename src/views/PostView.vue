<template>
    <el-input v-model="postTitle" :placeholder="$t('message.postTitle')" size="large" minlength="3" maxlength="50"
        show-word-limit>
    </el-input>
    <p class="alert">{{ a }}</p>
    <div class="foot-space"></div>
    <v-md-editor
        left-toolbar="undo redo | h bold italic strikethrough quote emoji | ul ol table hr todo-list | link image code tip"
        v-model="markdown" height="400px">
    </v-md-editor>
    <div class="foot-space"></div>
    <el-button @click="post()" type="primary">{{ $t('message.submit') }}</el-button>
</template>

<script>
export default {
    data() {
        return {
            postTitle: '',
            a: '',
            authkey: '',
            markdown: ''
        }
    },
    mounted() {
        this.markdown = ''
        var ak = localStorage.getItem('authkey')
        if (!ak) {
            this.$http.post("/api/authkey/v", {
                authkey: ak
            }).then((res) => {
                if (!res.data.data.authkey) {
                    this.$message.error(this.$t('message.loginFail'));
                    localStorage.removeItem('authkey')
                    this.$router.push("/login")
                }

            })

        }

    },
    methods: {
        checkTitle() {
            if (this.postTitle == '') {
                this.a = "填写此项"
                return false
            }
            if (this.postTitle.length < 3) {
                this.a = "帖子长度必须大于三个字符"
                return false
            }
            this.a = ""
            return true
        },
        post() {
            if (this.isEmpty(this.markdown)) {
                this.$message.error('内容不能为空');
                return false
            }
            if (this.checkTitle()) {
                this.$http.post('/api/post/write', {
                    title: this.postTitle,
                    content: this.markdown,
                    authkey: localStorage.getItem('authkey')
                }).then((res) => {
                    if (res.data.code = 200) {
                        this.$message.success(res.data.msg);
                        this.$message.success("您的帖子完成了审核!")
                        this.$router.push('/')
                    }
                })
            }


        },
        isEmpty(obj) {
            if (typeof obj == "undefined" || obj == null || obj == "") {
                return true;
            } else {
                return false;
            }
        }
    }
}
</script>
