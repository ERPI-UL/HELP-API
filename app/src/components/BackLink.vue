<template>
    <span class="flex items-center cursor-pointer" v-on:click="goBack()">
        <ChevronLeftIcon class="h-6"></ChevronLeftIcon>
        Back
    </span>
</template>

<script>
import { ChevronLeftIcon } from '@heroicons/vue/outline'
import { useRouter } from 'vue-router'

export default {
    name: 'BackLink',
    components: {
        ChevronLeftIcon,
    },
    setup() {
        const router = useRouter()

        const goBack = () => {
            router.back()
        }

        return {
            goBack
        }
    }
}
</script>

<style>

</style>