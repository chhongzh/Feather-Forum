<template>
  <div>
    <div class="foot-space"></div>
    <div>
      <el-card>
        <div>
          <el-row>
            <el-col :span="12">
              <el-card header="新成员">
                <div v-for="mem in mems" :key="mem">
                  <router-link :to='`/user/${mem.uid}`'>
                    <el-link>
                      {{ mem.name }}
                    </el-link>
                  </router-link>

                </div>
              </el-card>

            </el-col>
            <el-col :span="12">
              <el-card header="新帖子">
                <div v-for="pst in psts" :key="pst">
                  <router-link :to='`/post/${pst.pid}`'>
                    <el-link>
                      {{ pst.title }}
                    </el-link>
                  </router-link>

                </div>
              </el-card>
            </el-col>

          </el-row>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      members: 0,
      mems: {},
      psts: {},
      post: "",
      temp: ""
    }
  },
  mounted() {
    this.$http.get('/api/user/top').then((req) => {
      this.mems = req.data.data.list
    }).catch((req) => {
      this.$message.error('网络错误');
    })
  }

}
</script>

<style scoped>
</style>