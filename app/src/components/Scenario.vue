<template>
    <!-- Template Scenario card : Used to represent a scenario in a scenario list (for example in the scenario webpage) -->
    <div id="scenario-parent" class="bg-white rounded-lg shadow-lg p-4 min-w-fit h-fit max-w-[25vw] m-4 hover:shadow-xl">
        <div class="top">
            <div class="flex justify-between center">
                <h2 class="text-indigo-600 font-bold text-lg"> <!-- Scenario title -->
                    <slot name="title"></slot>
                </h2>
                <h2 class="ml-10 text-indigo-400 font-base text-base">
                    <slot name="machine"></slot> <!-- Scenario machine name -->
                </h2>
            </div>
            <p class="text-gray-400 text-base text-sm">
                <slot name="description"></slot> <!-- Scenario description -->
            </p>
        </div>
        <div class="pt-8 flex justify-between"> <!-- Scenario edit buttons (for edit mode) -->
            <div class="pr-10"><slot name="remove"></slot></div> <!-- Scenario remove button -->
            <slot name="href"></slot> <!-- Scenario edit/view redirect button -->
        </div>
    </div>
</template>

<script>

export default {
    name: "Scenario",
    components: {
        
    },
    setup: () => {
        return {}
    }
}
</script>
