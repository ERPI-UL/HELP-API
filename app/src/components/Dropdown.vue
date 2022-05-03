<template>
  <Menu as="div" class="relative inline-block text-left">
    <div>
      <MenuButton class="overflow-hidden inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 focus:ring-indigo-500">
        <slot name="label"></slot>
        <component :is="icon.user" class="flex-shrink-0 h-6 w-6 text-indigo-600" aria-hidden="true" />
      </MenuButton>
    </div>

    <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
        <MenuItems class="overflow-hidden origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
            <slot name="items" class="py-1">
                
            </slot>
        </MenuItems>
    </transition>
  </Menu>
</template>

<script>
import { Menu, MenuButton, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon, UserIcon } from '@heroicons/vue/solid'

export default {
  components: {
    Menu,
    MenuButton,
    MenuItems,
    ChevronDownIcon,
  },
  setup() {
      return {icon: {user: UserIcon}}
  }
}
</script>