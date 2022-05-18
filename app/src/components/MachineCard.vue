<template>
    <div class="scenario-parent bg-white rounded-lg shadow-lg p-4 w-fit h-fit min-w-[15vw] max-w-[25vw] m-4 hover:shadow-xl">
        <div class="top">
            <div class="flex justify-between center">
                <h2 class="text-indigo-600 font-bold text-lg">
                    <slot name="title"></slot>
                </h2>
            </div>
            <p class="text-gray-400 text-base text-sm mr-4">
                <slot name="description"></slot>
            </p>
        </div>
        <div class="pt-8 flex justify-between">
            <div class="pr-10">
                <slot name="remove"></slot>
            </div>
            <slot name="href"></slot>
        </div>
    </div>
</template>

<script>

export default {
    name: "MachineCard",
    components: {
        
    },
    setup: () => {
        return {user: JSON.parse(localStorage.getItem('user')??"{}")}
    }
}
</script>
