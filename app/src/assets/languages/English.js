const LANGUAGE = {  
    ACTIONS: {
        REGISTER: "register",
        LOGOUT: "logout",
        LOGIN: "login",
        CREATE: "create",
        EDIT: "edit",
        DELETE: "delete",
        ADD: "add",
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
        VIEW: "view",
        CHANGE: "change",
        SEND: "send",
        RESET: "reset",
        CHANGE: "change",
        UPDATE: "update",
        GENERATE: "generate"
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

    LOGS: {
        MODIFICATIONS_SAVED: "Modifications saved",
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
        SCENARIO_SELECTION: "scenario selection",
        LOADING_ERROR: "Loading error"
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
        },
        MESSAGES: {
            TITLE: "{action} a machine",
            MACHINE_NAME: "machine's name",
            MACHINE_DESCRIPTION: "machine's description",
            MACHINE_MODEL: "3D model",
            MACHINE_TARGETS: "machine's targets",
            ADD_MODEL: "add a model",
        },
        LOGS: {
            ERROR_MODEL_SAVING: "Error while saving the 3D model",
            SPECIFY_MACHINE_NAME: "Please specify a machine name",
            SPECIFY_MACHINE_DESCRIPTION: "Please specify a machine description",
            SPECIFY_TARGET_NAME: "Please specify a target name",
            DUPLICATE_TARGET_NAME: "Please specify unique target names",
            ERROR_CREATION: "Error while creating the machine",
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
        },
        MESSAGES: {
            MAIN_INFORMATIONS: "main informations",
            SCENARIO_NAME: "scenario's name",
            SCENARIO_DESCRIPTION: "scenario's description",
            TARGET_MACHINE: "target machine",
            STEPS: "steps",
            MODEL: "model",
            START: "start",
            END: "end",
            ACTION: "action",
            INFORMATION: "information",
            CHOICE: "choice",

            STEP_ID: "step identifier",
            STEP_TITLE: "step title",
            STEP_DESCRIPTION: "step description",
            STEP_TARGETS: "step targets",
            STEP_TYPE: "step type",
            BUTTON_CONFIG: "button configuration",
            LEFT_BTN_TEXT: "left button text",
            LEFT_BTN_TARGET: "left button target",
            RIGHT_BTN_TEXT: "right button text",
            RIGHT_BTN_TARGET: "right button target",
            TEXT_POSITION: "text position",
            INSERT_NEW_STEP: "insert a new step",

            SHOW_HIDE_CONTROLS: "show/hide controls",
            RESET_VIEW: "reset view"
        },
        LOGS: {
            SPECIFY_NAME: "Please specify a scenario name",
            SPECIFY_DESCRIPTION: "Please specify a scenario description",
            SELECT_MACHINE: "Please select a machine",
            AVOID_MACHINE_NAME: "Please avoid specifying the machine in the scenario name",
            CREATED: "Scenario successfully created",
            ERROR_CREATION: "Error while creating the scenario",
            MODIFIED: "Scenario successfully modified",
            ERROR_MODIFICATION: "Error while modifying the scenario",
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
        DESCRIPTION: "See and modify your profile",
        MESSAGES: {
            MODIFY_PASSWORD: "modify password",
            OLD_PASSWORD: "old password",
            NEW_PASSWORD: "new password",
        }
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
        },
        LOGS: {
            SPECIFY_USERNAME_EMAIL: "Please specify a username or email",
            INCORRECT_USERNAME_EMAIL: "Incorrect username or email",
            SERVER_ERROR: "Error during server communication"
        }
    },

    REGISTER: {
        MESSAGES: {
            CONFIRM_PASSWORD: "Confirm password",
        },
        LOGS: {
            SPECIFY_FIRSTNAME: "Please specify a firstname",
            SPECIFY_LASTNAME: "Please specify a lastname",
            SPECIFY_USERNAME: "Please specify a username",
            SPECIFY_EMAIL: "Please specify a valid email",
            SPECIFY_PASSWORD: "Please specify a password of at least 8 characters",
            SPECIFY_CONFIRM_PASSWORD: "Both passwords must match",
            CREATION_SUCCESS: "Account successfully created",
            CREATION_ERROR: "Error while creating the account"
        }
    },

    RESET: {
        MESSAGES: {
            TITLE: "{action} password"
        }
    }
}

export default LANGUAGE;