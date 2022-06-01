<template>
    <!-- Template topbar : header at the top of the website (with menus, login buttons, etc) -->
    <Popover class="relative bg-white shadow-lg rounded">
        <!-- START HEADER TOP BAR -->
        <div class="mx-auto px-3">
            <div class="flex justify-between items-center py-3 md:justify-start md:space-x-10">

                <!-- DESKTOP/MOBILE MENU VIEW -->
                <div class="flex justify-start lg:w-0 lg:flex-1"> <!-- Home indico icon -->
                    <a href="/" class="expand-parent flex">
                        <img class="h-8 w-auto sm:h-11 bg-indigo-600 border border-2 border-indigo-600 rounded-lg shadow-lg" src="../assets/images/icons/logo_white_indigo.png" alt="" />
                    </a>
                </div>

                <!-- MOBILE MENU VIEW -->
                <div class="-mr-2 -my-2 md:hidden"> <!-- Three horizontal line mobile menu -->
                    <PopoverButton
                        class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
                        <span class="sr-only">Open menu</span>
                        <MenuIcon class="h-6 w-6" aria-hidden="true" />
                    </PopoverButton>
                </div>

                <!-- DESKTOP MENU VIEW -->
                <PopoverGroup as="nav" class="hidden md:flex space-x-10">
                    <div v-for="opts in menu"> <!-- For each menu's elements, add a clickable label -->
                        
                        <div v-if="opts.href" class="text-gray-500 hover:text-gray-900"> <!-- if the element does not contains submenus, make a redirection label -->
                            <a :href="opts.href"> {{ opts.name }} </a>
                        </div>

                        <div v-if="opts.elements"> <!-- If the element contains submenus, add a popover containing the submenus -->
                            <Popover class="relative" v-slot="{ open }">
                                <!-- Add a clickable label to the menu (that will unwarp the submenu's list) -->
                                <PopoverButton :class="[open ? 'text-gray-900' : 'text-gray-500', 'group rounded-md inline-flex items-center text-base font-medium hover:text-gray-900']">
                                    <span> {{ opts.name }} </span>
                                    <ChevronDownIcon :class="[open ? 'text-gray-600' : 'text-gray-400', 'ml-2 h-5 w-5 group-hover:text-gray-500']" aria-hidden="true" />
                                </PopoverButton>
        
                                <!-- Submenu's list -->
                                <transition enter-active-class="transition ease-out duration-200"
                                    enter-from-class="opacity-0 translate-y-1" enter-to-class="opacity-100 translate-y-0"
                                    leave-active-class="transition ease-in duration-150"
                                    leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
                                    <PopoverPanel class="absolute z-10 -ml-4 mt-3 transform px-2 w-screen max-w-md sm:px-0 lg:ml-0 lg:left-1/2 lg:-translate-x-1/2">
                                        <div class="rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 overflow-hidden">
                                            <div class="relative grid gap-6 bg-white px-5 py-6 sm:gap-8 sm:p-8">
                                                <!-- For each elemen's submenu, add a redirection zone with the name,  description, and icon of the submenu -->
                                                <a v-for="item in opts.elements" :key="item.name" :href="item.href" class="-m-3 p-3 flex items-start rounded-lg hover:bg-gray-50">
                                                    <component :is="item.icon" class="flex-shrink-0 h-6 w-6 text-indigo-600" aria-hidden="true" />
                                                    <div class="ml-4">
                                                        <p class="text-base font-medium text-gray-900">{{ item.name }}</p>
                                                        <p class="mt-1 text-sm text-gray-500">{{ item.description }}</p>
                                                    </div>
                                                </a>
                                            </div>
                                        </div>
                                    </PopoverPanel>
                                </transition>
                            </Popover>
                        </div>
                    </div>
                </PopoverGroup>

                <!-- DESKTOP MENU VIEW -->
                <div class="hidden md:flex items-center justify-end md:flex-1 lg:w-0">
                    <div v-if="!User.isConnected(User.currentUser)"> <!-- If the user isn't connected, display login and register options -->
                        <a href="/register" class="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900"> S'inscrire </a>
                        <Redirectbutton href="/login" class="ml-3">Se connecter</Redirectbutton>
                    </div>
                    <div v-if="User.isConnected(User.currentUser)"> <!-- If the user is connected, display a dropdown button with his name -->
                        <Dropdown>
                            <template v-slot:label> <!-- Insert the user's firstname and lastname in the button's content -->
                                <p class="text-indigo-600 font-bold py-[2px] pr-2">{{ User.currentUser.firstname + " " + User.currentUser.lastname }}</p>
                            </template>
                            <template v-slot:items> <!-- Items showed in the dropdown's list when the button is clicked -->
                                <MenuItem v-slot="{ active }">
                                    <a href="/profile" :class="[active ? 'bg-indigo-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">Mon profil</a>
                                </MenuItem>
                                <MenuItem v-slot="{ active }">
                                    <a href="/easyconnect" :class="[active ? 'bg-indigo-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">Connecter un appareil</a>
                                </MenuItem>
                                <MenuItem v-slot="{ active }">
                                <button v-on:click="disconnect" :class="[active ? 'bg-indigo-100 text-gray-900' : 'text-gray-700', 'block w-full text-left px-4 py-2 text-sm']">Se déconnecter</button>
                                </MenuItem>
                            </template>
                        </Dropdown>
                    </div>
                </div>
            </div>
        </div>
        <!-- END HEADER TOP BAR -->

        <!-- MOBILE MENU VIEW (when the three horizontal lines are clicked) -->
        <transition enter-active-class="duration-200 ease-out" enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100" leave-active-class="duration-100 ease-in"
            leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
            <PopoverPanel focus class="z-50 absolute top-0 inset-x-0 p-2 transition transform origin-top-right md:hidden">
                <div class="rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 bg-white divide-y-2 divide-gray-50">
                    <div class="pt-5 pb-6 px-5">
                        <!-- LEFT USER BUTTON ZONE -->
                        <div class="flex items-center justify-between">
                            <!-- If the user isn't connected, simply display a Indico button -->
                            <div v-if="!User.isConnected(User.currentUser)">
                                <h3 class="text-indigo-600 font-semibold text-lg mt-1 ml-2 p-1 bg-indigo-50 rounded shadow border border-2 border-indigo-600"> Indico </h3>
                            </div>
                            <!-- If the user is connected, display it's username (shorter than firsname + lastname) and make the button redirect to it's profile -->
                            <div v-if="User.isConnected(User.currentUser)" class="mt-1 ml-2 p-1 rounded shadow-lg bg-indigo-50 cursor-pointer border border-2 border-indigo-600">
                                <a href="/profile" class="flex">
                                    <component :is="icon.user" class="flex-shrink-0 h-6 w-6 text-indigo-600" aria-hidden="true" />
                                    <h3 class="text-indigo-600 mx-1">{{User.currentUser.username}}</h3>
                                </a>
                            </div>
                            <!-- X button to close the menu -->
                            <div class="-mr-2">
                                <PopoverButton
                                    class="bg-white rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
                                    <span class="sr-only">Close menu</span>
                                    <XIcon class="h-6 w-6" aria-hidden="true" />
                                </PopoverButton>
                            </div>
                        </div>
                        <!-- MOBILE MENU CONTENT (menus and submenus) -->
                        <div class="mt-6">
                            <nav class="grid gap-y-6">
                                <div v-for="item in menu"> <!-- For each element in the meun -->
                                    <div class="px-2" v-if="item.href"> <!-- If the element does not have submenus, display a redirection label -->
                                        <a :key="item.name" :href="item.href" class="-m-3 pt-3 flex items-center rounded-md hover:bg-gray-50">
                                            <component :is="item.icon" class="flex-shrink-0 h-6 w-6 text-indigo-600" aria-hidden="true" />
                                            <span class="ml-3 text-base font-medium text-indigo-600">{{ item.name }}</span>
                                        </a>
                                    </div>
                                    <div class="px-2" v-if="item.elements"> <!-- If the element has submenus, display the label and all the submenus under it (shifted to the right) -->
                                        <p class="py-2">{{ item.name }}</p> <!-- Menu's label -->
                                        <!-- Element's submenus -->
                                        <a v-for="opts in item.elements" :key="opts.name" :href="opts.href" class="-m-3 p-2 flex items-center rounded-md hover:bg-gray-50">
                                            <component :is="item.icon" class="flex-shrink-0 h-6 w-6 text-indigo-600" aria-hidden="true" />
                                            <span class="ml-3 text-base font-medium text-indigo-600">{{ opts.name }}</span>
                                        </a>
                                    </div>
                                </div>
                            </nav>
                        </div>
                    </div>
                    <!-- MOBILE BOTTOM MENU -->
                    <div class="py-6 px-5 space-y-6">
                        <div v-if="!User.isConnected(User.currentUser)"> <!-- If the user isn't connected, display login and register options -->
                            <Redirectbutton href="/login" class="w-full">Se connecter</Redirectbutton>
                            <p class="mt-6 text-center text-base font-medium text-gray-500">
                                <a href="/register" class="text-indigo-600 hover:text-indigo-500">S'inscrire</a>
                            </p>
                        </div>
                        <div v-if="User.isConnected(User.currentUser)" class="text-center"> <!-- If the user is connected, display the log out button -->
                            <button v-on:click="disconnect" class="text-indigo-600 hover:text-indigo-500">Se déconnecter</button>
                        </div>
                    </div>
                </div>
            </PopoverPanel>
        </transition>
        <!-- END MOBILE MENU VIEW -->
    </Popover>
</template>

<script>
    import { Popover, PopoverButton, PopoverGroup, PopoverPanel, MenuItem } from '@headlessui/vue'
    import Dropdown from "./Dropdown.vue";
    import Redirectbutton from "../components/RedirectButton.vue";
    import User from "../script/User";

    import {
        MenuIcon,
        XIcon,
        AcademicCapIcon,
        PuzzleIcon,
        LinkIcon,
        EyeIcon,
        RefreshIcon,
        PencilAltIcon,
        TerminalIcon
    } from '@heroicons/vue/outline';
    import { ChevronDownIcon, UserIcon } from '@heroicons/vue/solid';

    /** Variable containing all the menu's options */
    let menu = [
        { // home button
            name: "Accueil",
            href: "/",
        },
        { // scenarios options (the other options are added later in the script depending on the user's role)
            name: "Scénarios",
            elements: [
                {
                    name: 'Tous les scénarios',
                    description: 'Voir les scénarios disponibles',
                    href: '/scenarios#all',
                    icon: EyeIcon
                }
            ]
        },
        { // machine options (the other options are added later in the script depending on the user's role)
            name: "Machines",
            elements: [
                {
                    name: 'Toutes les machines',
                    description: 'Voir les machines disponibles',
                    href: '/machines#all',
                    icon: EyeIcon
                }
            ]
        },
        { // statistics options
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
                    href: '/statistics#testing',
                    icon: AcademicCapIcon,
                }
            ]
        },
        { // other options (the administrator option is added later if the user is an administrator)
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
            if (User.currentUser.canLearner()) { // if the user is a learner, a teacher or an administrator, add the "my scenarios" option to the menu
                menu[menu.findIndex(el=>el.name=="Scénarios")].elements.push({
                    name: 'En cours',
                    description: 'Voir vos scénarios en cours',
                    href: '/scenarios#pending',
                    icon: RefreshIcon
                });
            }
            if (User.currentUser.canTeacher()) { // if the user is a teacher or an administrator, add the edit options to the menu
                menu[menu.findIndex(el=>el.name=="Scénarios")].elements.push({
                    name: 'Modifier',
                    description: 'Créer ou modifier un scénario',
                    href: '/scenarios#editing',
                    icon: PencilAltIcon
                });
                menu[menu.findIndex(el=>el.name=="Machines")].elements.push({
                    name: 'Modifier',
                    description: 'Créer ou modifier une machine',
                    href: '/machines#editing',
                    icon: PencilAltIcon
                });
            }
            if (User.currentUser.canAdmin()) { // if the user is an administrator, add the administrator panel to the menu
                menu[menu.findIndex(el=>el.name=="Autre")].elements.push({
                    name: 'Panneau administrateur',
                    description: 'Accéder au panneau d\'administration',
                    href: '/admin',
                    icon: TerminalIcon
                });
            }
            if (User.currentUser.isVisitor()) { // if the user is a visitor, remove the statistics options from the menu
                menu.splice(menu.findIndex(el=>el.name=="Statistiques"), 1);
            }

            return {menu, icon: {user: UserIcon}, User};
        },
        methods: {
            disconnect() { // log out the user
                User.forgetUser();
                window.location.href = '/';
            }
        }
    }
</script>