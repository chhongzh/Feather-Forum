<template>
  <div>
    <div>
      <transition name="el-fade-in-linear">
        <el-card v-show="allDone">
          <template #header><b>{{ config.forumName }}</b></template>
          <div>
            <el-row>
              <el-col :span="12">
                <el-card :header="$t('message.newMembers')">
                  <el-empty v-show="mems.length <= 0" :description="$t('message.noData')"></el-empty>
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
                <el-card :header="$t('message.newPost')">
                  <el-empty v-show="psts.length <= 0" :description="$t('message.noData')"></el-empty>
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

<script setup>
import config from '@/config/web'
</script>

<script>
export default {
  data() {
    return {
      mems: {},
      psts: {},
      post: "",
      temp: "",
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
        this.$message.error(this.$t('message.networkError'));
      })
    }).catch((req) => {
      this.$message.error(this.$t('message.networkError'));
    })

  }

}
</script>

<style scoped>

</style>