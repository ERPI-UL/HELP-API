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
        SEE: "see",
        CHANGE: "change",
        SEND: "send",
        RESET: "reset",
        CHANGE: "change",
    },

    EVENTS: {
        CONNECTED_TO: "Connected to {value}"
    },

    PAGES: {
        SCENARIOS: "scenarios",
        MACHINES: "machines",
        ACCOUNT: "account",
        STATISTICS: "statistics",
        HOME: "home",
        PROFILE: "profile",
        OTHER: "other",
        USERS: "users"
    },

    TIME: {
        SECOND: "second",
        SECONDS: "seconds",
        MINUTE: "minute",
        MINUTES: "minutes",
        DATE: "date",
        TIME: "time"
    },

    ROLES: {
        ADMIN: "admin",
        TEACHER: "teacher",
        LEARNER: "learner",
        VISITOR: "visitor"
    },

    COMMON: {
        AND: "and",
        OR: "or",
        ALL: "all",
        NONE: "none",
        MODE: "mode",
        OPTIONAL: "optional",

        FIRSTNAME: "firstname",
        LASTNAME: "lastname",
        USERNAME: "username",
        PASSWORD: "password",
        EMAIL: "email",
        ROLE: "role",

        SCENARIO: "scenario",
        MACHINE: "machine",
        USER: "user",
        STATISTIC: "statistic"
    },

    PAGINATION: {
        USER_SELECTION: "user selection",
        MACHINE_SELECTION: "machine selection",
        SCENARIO_SELECTION: "scenario selection"
    },

    HOME: {
        DESCRIPTION: "home page of the indico website",
        MESSAGES: {
            FREQUENTLY_USED: "frequently used",
            QUICK_ACCESS: "quick access",
            LAST_SESSION: "last session",
            NO_LAST_SESSION_FOUND: "no last session found",
            MODAL: {
                TITLE: "Indico - Web Interface",
                DESCRIPTION: "This is the web interface of the Indico project. It allows you to manage your scenarios, machines and users.",
            }
        }
    },

    LOGIN: {
        
    },

    STATISTICS: {
        PAGES: {
            LEARNING: {
                TITLE: "learning mode",
                REDIRECT: "see my stats",
                DESCRIPTION: "see my stats in learning mode",

            },
            TESTING: {
                TITLE: "evaluation mode",
                REDIRECT: "see my stats",
                DESCRIPTION: "see my stats in evaluation mode",

            },
        },
        ABS_TIME: "absolute time",
        MESSAGES: {
            LOADING_DATA: {
                TITLE: "loading ...",
                DESCRIPTION: "loading statistics",
            },
            NO_DATA: {
                TITLE: "no data",
                DESCRIPTION: "no data available for the selected filters",
            },
            PROBLEM_DATA: {
                TITLE: "Houston, we have a problem",
                DESCRIPTION: "Cannot retreive statistics from the server",
            }
        }
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
        },
        ACTIONS: {
            NEW: "new machine",
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
        DESCRIPTION: "connect a device to your account",
        MESSAGES: {
            CONNECT_DEVICE: "connect a device",
            DEVICE_CODE: "device code"
        }
    },

    INVITE: {
        TITLE: "Invite a user",
        REDIRECT: "Invite",
        DESCRIPTION: "Send an invite link to a future user",
        MESSAGES: {
            GENERATE_INVITE: "Generate invite",
            VALIDATION_DELAY: "This invitation will be valid for 14 days from its creation date"
        }
    },

    PROFILE: {
        TITLE: "my profile",
        REDIRECT: "my profile",
        DESCRIPTION: "See and modify your profile"
    },

    ADMIN: {
        TITLE: "administation",
        REDIRECT: "see admin panel",
        DESCRIPTION: "see and manage the application",
        MESSAGES: {
            SELECT_USER: "Select a user",
            CHANGE_ROLE: "Change role",
            REMOVE_USER: "Remove user",
            USER_SESSIONS: "User sessions",
        }
    },

    ABOUT: {
        TITLE: "about page",
        REDIRECT: "go to about",
        DESCRIPTION: "See all the informations about Indico",
        MESSAGES: {
            WITH_GRANDEST_SUPPORT: "with Grand Est region financial support",
            INDICO_VERSION: "Indico - version {version}"
        }
    },

    FORGOTPASSWORD: {
        MESSAGES: {
            FORGOT_PASSWORD: "Forgot password",
            DESCRIPTION: "After entering your username or email, you will receive instructions to reset your password in the mailbox associated with your account.",
        }
    },

    REGISTER: {
        MESSAGES: {
            CONFIRM_PASSWORD: "Confirm password",
        }
    },

    RESET: {
        MESSAGES: {
            TITLE: "{action} password"
        }
    }
}

export default LANGUAGE;