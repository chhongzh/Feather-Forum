<template>
  <div>
    <div>
      <transition name="el-fade-in-linear">
        <el-card v-show="allDone">
          <template #header><b>{{ forum }}</b></template>
          <div>
            <el-row>
              <el-col :span="12">
                <el-card header="新成员">
                  <el-empty v-show="mems.length <= 0" description="没有数据"></el-empty>
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
                  <el-empty v-show="psts.length <= 0" description="没有数据"></el-empty>
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
      </transition>
    </div>
  </div>
</template>

<script>
import config from '../assets/js/config.js'
export default {
  data() {
    return {
      members: 0,
      mems: {},
      psts: {},
      post: "",
      temp: "",
      forum: '',
      allDone: false
    }
  },
  mounted() {
    this.$http.get('/api/user/top').then((req) => {
      this.mems = req.data.data.list
      this.$http.get('/api/post/top').then((req) => {
        this.psts = req.data.data.list
        this.allDone = true
      }).catch((req) => {
        this.$message.error('网络错误');
      })
    }).catch((req) => {
      this.$message.error('网络错误');
    })

    this.forum = config.forumName
  }

}
</script>

<style scoped>

</style>