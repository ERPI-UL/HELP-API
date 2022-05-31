<template>
    <!-- Template Validate Ppopup : popup showing up on top of other components to validate an action (for example account deletion) -->
    <div v-show="this.obj.showing" class="flex w-screen h-screen absolute top-0 left-0 pointer-events-none bg-black/[0.2]">
        <div v-show="this.obj.showing" class="pointer-events-auto fixed rounded-lg shadow-lg border border-1 border-gray-300 p-2 bg-white">
            <!-- Popup title and description -->
            <div id="text" class="divide-y">
                <h2 class="text-left font-semibold text-gray-600 text-lg m-1">{{ this.obj.title }}</h2>
                <p class="text-center font-base text-gray-500 text-medium px-8 py-2 m-1">{{ this.obj.infos }}</p>
            </div>
            <!-- Popup options (cancel and validate action) -->
            <div id="controls" class="flex grow justify-between">
                <CancelButton v-on:click="this.hide();" class="mr-8">{{ this.obj.cancelLabel }}</CancelButton> <!-- Cancel button -->
                <!-- Validate button (dangerous style because if a popup is shown, it's probably for a important action) -->
                <DangerousButton v-on:click="this.obj.validateCallback(); this.hide();">{{ this.obj.validateLabel }}</DangerousButton>
            </div>
        </div>
    </div>
</template>

<script>
import CancelButton from "../components/CancelButton.vue";
import ValidateButton from "../components/ValidateButton.vue";
import DangerousButton from "../components/DangerousButton.vue";

/**
 * Represents the current Validate Popup
 */
class ValidatePopup {
    showing = false;
    cancelLabel = "Annuler";
    validateLabel = "Valider";
    title = "";
    infos = "";
    validateCallback = () => {}
}

export default {
    name: "ValidatePopup",
    props: [],
    components: {
        CancelButton,
        ValidateButton,
        DangerousButton
    },
    data() { return {obj: new ValidatePopup()}; },
    methods: {
        /**
         * Shows the popup, applying the new title, description, buttons labels
         */
        show(title="", infos="", cancelLabel="", validateLabel="") {
            this.obj.title = title;
            this.obj.infos = infos;
            this.obj.cancelLabel = cancelLabel;
            this.obj.validateLabel = validateLabel;
            this.obj.showing = true;
            this.$el.style.opacity = "0";
        },
        /**
         * hides the popup
         */
        hide() {
            this.$el.style.opacity = "0";
            setTimeout(() => {
                this.obj.showing = false;
            }, 200);
        },
        /**
         * Moved the popup position on top of the given element
         * @param {HTMLElement} dom the element to move on top of
         */
        setPosition(dom) {
            setTimeout(() => {
                const el = this.$el.firstChild;
                const domRect = dom.getBoundingClientRect();
                const elRect = el.getBoundingClientRect();
                
                // ON TOP
                el.style.top = domRect.top - elRect.height - 10 + "px";
                el.style.left = domRect.left + domRect.width/2 - (elRect.width/2) + "px";

                // IF NOT ENOUGH PLACE, GO ON BOTTOM
                if (el.style.top < 5) {
                    el.style.top = domRect.top + domRect.height + 10 + "px";
                    el.style.left = domRect.left + domRect.width/2 - (elRect.width/2) + "px";
                }

                if (this.obj.showing) {
                    el.style.animation = "none";
                    el.style.transform = "scale(0.9, 0)";
                    el.style.transformOrigin = "50% 100%";
                    setTimeout(() => {
                        el.style.animation = "";
                        el.style.transform = "scale(1, 1)";
                        this.$el.style.opacity = "1";
                    }, 40);
                }
            }, 30);
        },
        /**
         * Assigns the new validate callback to execute when the user clicks on the validate button
         */
        setCallback(callback) {
            this.obj.validateCallback = callback;
        }
    }
}
</script>