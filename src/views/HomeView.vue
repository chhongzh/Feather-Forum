<template>
  <!-- <div class="first"> -->
  <!-- <img src="../assets/background-1.png" alt=""> -->
  <!-- <div class="mask"></div> -->
  <!-- <div class="box"/> -->
  <!-- <h1>Apple_qwq ?</h1> -->
  <!-- </div> -->
  <!-- </div> -->
  <div>
    <div>
      <el-card>
        <template #header>
          <div class="card-header">
            <span class="h2">公告</span>
          </div>
        </template>
        <div v-html="post"></div>
      </el-card>
    </div>
    <div class="foot-space"></div>
    <div>
      <el-card>
        <template #header>
          <div class="card-header">
            <span class="h2">统计</span>
          </div>
        </template>
        <div>
          <el-row>
            <el-col :span="12">
              <h4>共有:{{ members }}个会员</h4>
            </el-col>
            <el-col :span="12">
              <h4>共有:{{}}个帖子</h4>
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
      post: ""
    }
  },
  mounted() {
    this.$http.get('/api/user/count').then((req) => {
      console.log(req)
    }).catch((req) => {
      this.$message.error('网络错误');
    })
  }

}
</script>

<style scoped>
</style>