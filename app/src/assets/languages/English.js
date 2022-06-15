const LANGUAGE = {  
    ACTIONS: {
        REGISTER: "register",
        LOGOUT: "logout",
        LOGIN: "login",
        CREATE: "create",
        EDIT: "edit",
        DELETE: "delete",
        SAVE: "save",
        CANCEL: "cancel",
        VALIDATE: "validate",
        REMOVE: "remove",
        BACK: "back",
        LOADING: "loading",
        SEARCH: "search",
        CONNECT: "connect",
        MORE: "more",
        SELECT: "select",
        SEE: "see"
    },

    PAGES: {
        SCENARIOS: "scenarios",
        MACHINES: "machines",
        ACCOUNT: "account",
        STATISTICS: "statistics",
        HOME: "home",
        PROFILE: "profile",
        OTHER: "other"
    },

    TIME: {
        SECOND: "second",
        SECONDS: "seconds",
        MINUTE: "minute",
        MINUTES: "minutes",
        DATE: "date",
        TIME: "time"
    },

    COMMON: {
        WORDS: {
            AND: "and",
            OR: "or",
            ALL: "all",
            NONE: "none"
        },

        SCENARIO: "scenario",
        MACHINE: "machine",
        USER: "user",
        STATISTIC: "statistic"
    },

    HOME: {
        DESCRIPTION: "home page of the indico website",
        FREQUENTLY_USED: "frequently used",
        QUICK_ACCESS: "quick access",
        WITH_GRANDEST_SUPPORT: "with Grand Est region financial support",
        LAST_SESSION: "last session",
        NO_LAST_SESSION_FOUND: "no last session found"
    },

    STATISTICS: {
        PAGES: {
            LEARNING: {
                TITLE: "learning mode",
                REDIRECT: "see my stats",
                DESCRIPTION: "see my stats in learning mode",

            },
            TESTING: {
                TITLE: "testing mode",
                REDIRECT: "see my stats",
                DESCRIPTION: "see my stats in testing mode",

            },
        },
        ABS_TIME: "absolute time",
    },

    MACHINES: {
        PAGES: {
            VIEW: {
                TITLE: "see all machines",
                REDIRECT: "see all machines",
                DESCRIPTION: "see all available machines"
            },
            EDIT: {
                TITLE: "edit machines",
                REDIRECT: "edit machines",
                DESCRIPTION: "edit or remove a machine"
            },
            CREATE: {
                TITLE: "create a machine",
                REDIRECT: "create a machine",
                DESCRIPTION: "create a new machine"
            }
        }
    },

    SCENARIOS: {
        PAGES: {
            VIEW: {
                TITLE: "see all scenarios",
                REDIRECT: "see all scenarios",
                DESCRIPTION: "see all available scenarios"
            },
            OWN: {
                TITLE: "see own scenarios",
                REDIRECT: "see own scenarios",
                DESCRIPTION: "see my own scenarios"
            },
            EDIT: {
                TITLE: "edit scenarios",
                REDIRECT: "edit scenarios",
                DESCRIPTION: "edit or remove a scenario"
            },
            CREATE: {
                TITLE: "create a scenario",
                REDIRECT: "create a scenario",
                DESCRIPTION: "create a new scenario"
            }
        },
        ACTIONS: {
            REMOVE: {
                TITLE: "remove scenario",
                DESCRIPTION: "Do you want to remove this scenario ?"
            },
            NEW: "new scenario",
        }
    },

    EASYCONNECT: {
        TITLE: "Easy Connect",
        REDIRECT: "connect a device",
        DESCRIPTION: "connect a device to your account"
    },

    INVITE: {
        TITLE: "Invite a user",
        REDIRECT: "Invite",
        DESCRIPTION: "Send an invite link to a future user"
    },

    PROFILE: {
        TITLE: "my profile",
        REDIRECT: "my profile",
        DESCRIPTION: "See and modify your profile"
    },

    ADMIN: {
        TITLE: "administation",
        REDIRECT: "see admin panel",
        DESCRIPTION: "see and manage the application"
    },

    ABOUT: {
        TITLE: "about page",
        REDIRECT: "go to about",
        DESCRIPTION: "See all the informations about Indico"
    }
}

export default LANGUAGE;