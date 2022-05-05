<template>
    <Popover class="relative bg-white shadow-lg rounded">
        <div class="mx-auto px-3">
            <div
                class="flex justify-between items-center py-3 md:justify-start md:space-x-10">
                <div class="flex justify-start lg:w-0 lg:flex-1">
                    <a href="/">
                        <span class="sr-only">Workflow</span>
                        <img class="h-8 w-auto sm:h-11" src="../assets/images/icons/icon_full.png" alt="" />
                    </a>
                </div>
                <div class="-mr-2 -my-2 md:hidden">
                    <PopoverButton
                        class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
                        <span class="sr-only">Open menu</span>
                        <MenuIcon class="h-6 w-6" aria-hidden="true" />
                    </PopoverButton>
                </div>

                <PopoverGroup as="nav" class="hidden md:flex space-x-10">
                    <div v-for="opts in menu">
                        <div v-if="opts.href">
                            <a href="#"> {{ opts.name }} </a>
                        </div>
                        <div v-if="opts.elements">
                            <Popover class="relative" v-slot="{ open }">
                                <PopoverButton
                                    :class="[open ? 'text-gray-900' : 'text-gray-500', 'group bg-white rounded-md inline-flex items-center text-base font-medium hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500']">
                                    <span> {{ opts.name }} </span>
                                    <ChevronDownIcon
                                        :class="[open ? 'text-gray-600' : 'text-gray-400', 'ml-2 h-5 w-5 group-hover:text-gray-500']"
                                        aria-hidden="true" />
                                </PopoverButton>
        
                                <transition enter-active-class="transition ease-out duration-200"
                                    enter-from-class="opacity-0 translate-y-1" enter-to-class="opacity-100 translate-y-0"
                                    leave-active-class="transition ease-in duration-150"
                                    leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
                                    <PopoverPanel
                                        class="absolute z-10 -ml-4 mt-3 transform px-2 w-screen max-w-md sm:px-0 lg:ml-0 lg:left-1/2 lg:-translate-x-1/2">
                                        <div class="rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 overflow-hidden">
                                            <div class="relative grid gap-6 bg-white px-5 py-6 sm:gap-8 sm:p-8">
                                                <a v-for="item in opts.elements" :key="item.name" :href="item.href"
                                                    class="-m-3 p-3 flex items-start rounded-lg hover:bg-gray-50">
                                                    <component :is="item.icon" class="flex-shrink-0 h-6 w-6 text-indigo-600"
                                                        aria-hidden="true" />
                                                    <div class="ml-4">
                                                        <p class="text-base font-medium text-gray-900">
                                                            {{ item.name }}
                                                        </p>
                                                        <p class="mt-1 text-sm text-gray-500">
                                                            {{ item.description }}
                                                        </p>
                                                    </div>
                                                </a>
                                            </div>
                                            <!-- <div
                                                class="px-5 py-5 bg-gray-50 space-y-6 sm:flex sm:space-y-0 sm:space-x-10 sm:px-8">
                                                <div v-for="item in callsToAction" :key="item.name" class="flow-root">
                                                    <a :href="item.href"
                                                        class="-m-3 p-3 flex items-center rounded-md text-base font-medium text-gray-900 hover:bg-gray-100">
                                                        <component :is="item.icon" class="flex-shrink-0 h-6 w-6 text-gray-400"
                                                            aria-hidden="true" />
                                                        <span class="ml-3">{{ item.name }}</span>
                                                    </a>
                                                </div>
                                            </div> -->
                                        </div>
                                    </PopoverPanel>
                                </transition>
                            </Popover>
                        </div>
                    </div>
                </PopoverGroup>
                

                <div class="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
                    <div v-if="!user.connected">
                        <a href="/register" class="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900"> S'inscrire </a>
                        <Redirectbutton href="/login" class="ml-3">
                            Se connecter
                        </Redirectbutton>
                    </div>
                    <div v-if="user.connected">
                        <Dropdown>
                            <template v-slot:label>
                                <p class="text-indigo-600 font-bold py-[2px] pr-2">{{ user.username }}</p>
                            </template>
                            <template v-slot:items>
                                <MenuItem v-slot="{ active }">
                                    <a href="/" :class="[active ? 'bg-purple-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">Mon profil</a>
                                </MenuItem>
                                <MenuItem v-slot="{ active }">
                                    <a href="/easyconnect" :class="[active ? 'bg-purple-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">Connecter un appareil</a>
                                </MenuItem>
                                <form method="POST" action="/">
                                    <MenuItem v-slot="{ active }">
                                    <button type="submit" :class="[active ? 'bg-purple-100 text-gray-900' : 'text-gray-700', 'block w-full text-left px-4 py-2 text-sm']">Se déconnecter</button>
                                    </MenuItem>
                                </form>
                            </template>
                        </Dropdown>
                    </div>
                </div>
            </div>
        </div>

        <transition enter-active-class="duration-200 ease-out" enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100" leave-active-class="duration-100 ease-in"
            leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
            <PopoverPanel focus class="z-50 absolute top-0 inset-x-0 p-2 transition transform origin-top-right md:hidden">
                <div class="rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 bg-white divide-y-2 divide-gray-50">
                    <div class="pt-5 pb-6 px-5">
                        <div class="flex items-center justify-between">
                            <div>
                                <img class="h-8 w-auto" src="../assets/images/icons/icon_full.png" alt="Workflow" />
                            </div>
                            <div class="-mr-2">
                                <PopoverButton
                                    class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
                                    <span class="sr-only">Close menu</span>
                                    <XIcon class="h-6 w-6" aria-hidden="true" />
                                </PopoverButton>
                            </div>
                        </div>
                        <div class="mt-6">
                            <nav class="grid gap-y-8">
                                <div v-for="item in menu">
                                    <div class="ps-4" v-if="item.href">
                                        <a :key="item.name" :href="item.href"
                                            class="-m-3 p-3 flex items-center rounded-md hover:bg-gray-50">
                                            <component :is="item.icon" class="flex-shrink-0 h-6 w-6 text-indigo-600"
                                                aria-hidden="true" />
                                            <span class="ml-3 text-base font-medium text-gray-900">
                                                {{ item.name }}
                                            </span>
                                        </a>
                                    </div>
                                    <div class="px-4" v-if="item.elements">
                                        <p class="py-2">{{ item.name }}</p>
                                        <a v-for="opts in item.elements" :key="opts.name" :href="opts.href"
                                            class="-m-3 p-3 flex items-center rounded-md hover:bg-gray-50">
                                            <component :is="item.icon" class="flex-shrink-0 h-6 w-6 text-indigo-600"
                                                aria-hidden="true" />
                                            <span class="ml-3 text-base font-medium text-gray-900">
                                                {{ opts.name }}
                                            </span>
                                        </a>
                                    </div>
                                </div>
                            </nav>
                        </div>
                    </div>
                    <div class="py-6 px-5 space-y-6">
                        <div>
                            <Redirectbutton href="/login" class="w-full">
                                Se connecter
                            </Redirectbutton>
                            <p class="mt-6 text-center text-base font-medium text-gray-500">
                                <a href="/register" class="text-indigo-600 hover:text-indigo-500">S'inscrire</a>
                            </p>
                        </div>
                    </div>
                </div>
            </PopoverPanel>
        </transition>
    </Popover>
</template>

<script>
    import { Popover, PopoverButton, PopoverGroup, PopoverPanel, MenuItem } from '@headlessui/vue'
    import Dropdown from "./Dropdown.vue";
    import Redirectbutton from "../components/RedirectButton.vue";

    import {
        MenuIcon,
        XIcon,
        AcademicCapIcon,
        PuzzleIcon,
        LinkIcon,
        EyeIcon,
        RefreshIcon,
        CheckIcon
    } from '@heroicons/vue/outline'
    import { ChevronDownIcon } from '@heroicons/vue/solid'

    const menu = [
        {
            name: "Scénarios",
            elements: [
                {
                    name: 'Voir les scénarios',
                    description: 'Voir les scénarios disponibles',
                    href: '/scenarios#all',
                    icon: EyeIcon
                },
                {
                    name: 'Mes scénarios',
                    description: 'Voir vos scénarios en cours',
                    href: '/scenarios#pending',
                    icon: RefreshIcon
                },
                {
                    name: 'Complétés',
                    description: 'Voir vos scénarios complétés',
                    href: '/scenarios#completed',
                    icon: CheckIcon
                }
            ]
        },
        {
            name: "Statistiques",
            elements: [
                {
                    name: 'Apprentissage',
                    description: 'Voir les statistiques dans le mode apprentissage',
                    href: '/statistics#learning',
                    icon: PuzzleIcon,
                },
                {
                    name: 'Évalutation',
                    description: 'Voir les statistiques dans le mode évaluation',
                    href: 'statistics#testing',
                    icon: AcademicCapIcon,
                }
            ]
        },
        {
            name: "Autre",
            elements: [
                {
                    name: 'Connecter un appareil',
                    description: 'Connecter un appareil à votre compte',
                    href: '/easyconnect',
                    icon: LinkIcon,
                }
            ]
        }
    ];

    export default {
        components: {
            Popover,
            PopoverButton,
            PopoverGroup,
            PopoverPanel,
            ChevronDownIcon,
            MenuIcon,
            XIcon,
            Dropdown,
            MenuItem,
            Redirectbutton
        },
        setup() {
            return {menu, user: JSON.parse(localStorage.getItem('user')??"{}")};
        }
    }
</script>