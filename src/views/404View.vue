<template>
    <div>
        <h1>{{ $t('message.notFoundTitle') }}</h1>
        <p>{{ $t('message.notFoundCheckUrl') }}</p>
        <router-link to="/">
            <el-link type="primary">{{ $t('message.backHome') }}</el-link>
        </router-link>

    </div>
</template>

<script>
export default {

}
</script>

<style>

</style>