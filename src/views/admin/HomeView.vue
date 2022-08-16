<template>
    <div>
        <el-row>
            <el-col :span="4">
                <el-card shadow="hover" header="用户总数">{{ userTotal }}</el-card>
            </el-col>
            <el-col :span="4">
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    data() {
        return {
            userTotal: 0
        }
    }
}
</script>

<style>
.--ff-box {
    background-color: blue;
    width: 100%;
    height: 150px;
    border-radius: 20px
}
</style>