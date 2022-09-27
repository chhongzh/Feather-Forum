<template>
    <el-input v-model="postTitle" placeholder="帖子标题" size="large" minlength="3" maxlength="50" show-word-limit>
    </el-input>
    <p class="alert">{{ a }}</p>
    <div class="foot-space"></div>
    <v-md-editor
        left-toolbar="undo redo | h bold italic strikethrough quote emoji | ul ol table hr todo-list | link image code tip"
        v-model="markdown" height="400px">
    </v-md-editor>
    <v-md-editor v-model="markdown" height="400px"></v-md-editor>
    <div class="foot-space"></div>
    <el-button @click="post()" type="primary">提交</el-button>
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
                    this.$message.error('未登录或登录过期,请重新登陆');
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

<style>
/* html.dark {
    --w-e-textarea-bg-color: var(--el-bg-color);
    --w-e-textarea-color: #EBEDF0;
    --w-e-textarea-border-color: #D4D7DE;
    --w-e-textarea-slight-border-color: #D4D7DE;
    --w-e-textarea-slight-color: #d4d4d4;
    --w-e-textarea-slight-bg-color: var(--el-bg-color);
    --w-e-textarea-selected-border-color: #B4D5FF;
    --w-e-textarea-handler-bg-color: #4290f7;

    --w-e-toolbar-color: #FFFFFF;
    --w-e-toolbar-bg-color: var(--el-bg-color);
    --w-e-toolbar-active-color: #333;
    --w-e-toolbar-active-bg-color: var(--el-bg-color);
    --w-e-toolbar-disabled-color: var(--el-color-info-dark-2);
    --w-e-toolbar-border-color: #D4D7DE;


    --w-e-modal-button-bg-color: var(--el-bg-color);
    --w-e-modal-button-border-color: #d9d9d9;
   
} */
</style>