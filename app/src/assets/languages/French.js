const LANGUAGE = {  
    ACTIONS: {
        REGISTER: "s'inscrire",
        LOGOUT: "se déconnecter",
        LOGIN: "se connecter",
        CREATE: "créer",
        EDIT: "modifier",
        DELETE: "supprimer",
        ADD: "ajouter",
        SAVE: "sauvegarder",
        CANCEL: "annuler",
        VALIDATE: "valider",
        BACK: "retour",
        LOADING: "chargement",
        SEARCH: "chercher",
        CONNECT: "connecter",
        MORE: "plus",
        SELECT: "selectionner",
        VIEW: "voir",
        CHANGE: "changer",
        SEND: "envoyer",
        RESET: "réinitialiser",
        CHANGE: "changer",
        UPDATE: "mettre à jour",
        GENERATE: "générer"
    },

    EVENTS: {
        CONNECTED_TO: "connecté à {value}"
    },

    PAGES: {
        SCENARIOS: "scénarios",
        MACHINES: "machines",
        ACCOUNT: "compte",
        STATISTICS: "statistiques",
        HOME: "accueil",
        PROFILE: "profile",
        OTHER: "autres",
        USERS: "utilisateurs"
    },

    TIME: {
        SECOND: "seconde",
        SECONDS: "secondes",
        MINUTE: "minute",
        MINUTES: "minutes",
        DATE: "date",
        TIME: "temps"
    },

    ROLES: {
        ADMIN: "administrateur",
        TEACHER: "professeur",
        LEARNER: "apprenti",
        VISITOR: "visiteur"
    },

    LOGS: {
        MODIFICATIONS_SAVED: "Modifications sauvegardées",
    },

    COMMON: {
        AND: "et",
        OR: "ou",
        ALL: "Tous",
        NONE: "Aucun",
        MODE: "mode",
        OPTIONAL: "optionel",

        LANGUAGE: "langage",
        FIRSTNAME: "prénom",
        LASTNAME: "nom",
        USERNAME: "nom d'utilisateur",
        PASSWORD: "mot de passe",
        EMAIL: "Adresse mail",
        ROLE: "rôle",

        SCENARIO: "scénario",
        MACHINE: "machine",
        USER: "utilisateur",
        STATISTIC: "statistique"
    },

    PAGINATION: {
        USER_SELECTION: "séléction utilisateurs",
        MACHINE_SELECTION: "séléction machines",
        SCENARIO_SELECTION: "séléction scénarios",
        LOADING_ERROR: "erreur de chargement"
    },

    HOME: {
        DESCRIPTION: "page d'accueil de l'interface web d'Indico",
        MESSAGES: {
            FREQUENTLY_USED: "fréquement utilisés",
            QUICK_ACCESS: "Accès rapide",
            LAST_SESSION: "Dernière session",
            NO_LAST_SESSION_FOUND: "Aucune dernière session trouvée",
            MODAL: {
                TITLE: "Indico - Interface web",
                DESCRIPTION: "Ceci est l'interface web de l'application Indico. Vous pouvez y accéder gérer vos scénarios, vos machines et autres.",
            }
        }
    },

    STATISTICS: {
        PAGES: {
            LEARNING: {
                TITLE: "mode apprentissage",
                REDIRECT: "Voir mes statistiques",
                DESCRIPTION: "Voir mes statistiques en mode apprentissage",

            },
            TESTING: {
                TITLE: "mode évaluation",
                REDIRECT: "Voir mes statistiques",
                DESCRIPTION: "Voir mes statistiques en mode évaluation",

            },
        },
        ABS_TIME: "Temps absolu",
        MESSAGES: {
            LOADING_DATA: {
                TITLE: "Chargement ...",
                DESCRIPTION: "Chargement des statistiques ...",
            },
            NO_DATA: {
                TITLE: "Aucune donnée",
                DESCRIPTION: "Aucune donnée disponible pour les filtres sélectionnés",
            },
            PROBLEM_DATA: {
                TITLE: "Houston, nous avons un problème",
                DESCRIPTION: "Impossible de récupérer les données",
            }
        }
    },

    MACHINES: {
        PAGES: {
            VIEW: {
                TITLE: "Voir toutes les machines",
                REDIRECT: "Voir les machines",
                DESCRIPTION: "Voir toutes les machines disponibles"
            },
            EDIT: {
                TITLE: "Modifier une machine",
                REDIRECT: "Modifier une machine",
                DESCRIPTION: "Modifier ou supprimer une machine"
            },
            CREATE: {
                TITLE: "Créer une machine",
                REDIRECT: "Créer une machine",
                DESCRIPTION: "Créer une nouvelle machine"
            }
        },
        ACTIONS: {
            REMOVE: {
                TITLE: "Supprimer la machine",
                DESCRIPTION: "Voulez-vous supprimer cette machine ?",
            },
            NEW: "Nouvelle machine",
        },
        MESSAGES: {
            TITLE: "{action} une machine",
            MACHINE_NAME: "Nom de la machine",
            MACHINE_DESCRIPTION: "Description de la machine",
            MACHINE_MODEL: "Modèle 3D",
            MACHINE_TARGETS: "Cibles de la machine",
            ADD_MODEL: "Ajouter une modèle",
        },
        LOGS: {
            ERROR_MODEL_SAVING: "Erreur lors de la sauvegarde du modèle 3D",
            SPECIFY_MACHINE_NAME: "Veuillez spécifier un nom de machine",
            SPECIFY_MACHINE_DESCRIPTION: "Veuillez spécifier une description de machine",
            SPECIFY_TARGET_NAME: "Veuillez spécifier un nom de cible",
            DUPLICATE_TARGET_NAME: "Veuillez spécifier des noms de cible unique",
            ERROR_CREATION: "Erreur lors de la création de la machine",
            CREATED: "Machine créée avec succès",
            ALREADY_EXISTS: "La machine existe déjà",
        }
    },

    SCENARIOS: {
        PAGES: {
            VIEW: {
                TITLE: "voir tous les scénarios",
                REDIRECT: "voir les scénarios",
                DESCRIPTION: "voir tous les scénarios disponibles"
            },
            OWN: {
                TITLE: "Voir mes scénarios",
                REDIRECT: "Voir mes scénarios",
                DESCRIPTION: "Voir mes scénarios commencés"
            },
            EDIT: {
                TITLE: "Modifier un scénario",
                REDIRECT: "Modifier un scénario",
                DESCRIPTION: "Modifier ou supprimer un scénario"
            },
            CREATE: {
                TITLE: "Créer un scénario",
                REDIRECT: "Créer un scénario",
                DESCRIPTION: "Créer un nouveau scénario"
            }
        },
        ACTIONS: {
            REMOVE: {
                TITLE: "Supprimer le scénario",
                DESCRIPTION: "Voulez-vous supprimer ce scénario ?",
            },
            NEW: "Nouveau scénario",
        },
        MESSAGES: {
            MAIN_INFORMATIONS: "Informations principales",
            SCENARIO_NAME: "Nom du scénario",
            SCENARIO_DESCRIPTION: "Description du scénario",
            TARGET_MACHINE: "Machine cible",
            STEPS: "Etapes",
            MODEL: "Modèle",
            START: "Début",
            END: "Fin",
            ACTION: "action",
            INFORMATION: "information",
            CHOICE: "choix",

            STEP_ID: "identifiant de l'étape",
            STEP_TITLE: "titre de l'étape",
            STEP_DESCRIPTION: "description de l'étape",
            STEP_TARGETS: "cibles de l'étape",
            STEP_TYPE: "type d'étape",
            BUTTON_CONFIG: "configuration des boutons",
            LEFT_BTN_TEXT: "texte du bouton gauche",
            LEFT_BTN_TARGET: "cible du bouton gauche",
            RIGHT_BTN_TEXT: "texte du bouton droit",
            RIGHT_BTN_TARGET: "cible du bouton droit",
            TEXT_POSITION: "position du texte",
            INSERT_NEW_STEP: "insérer une nouvelle étape",

            SHOW_HIDE_CONTROLS: "Afficher/Cacher les contrôles",
            RESET_VIEW: "Réinitialiser la vue",
        },
        LOGS: {
            SPECIFY_NAME: "Veuillez spécifier un nom de scénario",
            SPECIFY_DESCRIPTION: "Veuillez spécifier une description de scénario",
            SELECT_MACHINE: "Veuillez sélectionner une machine",
            AVOID_MACHINE_NAME: "Evitez de spécifier la machine dans le nom du scénario",
            CREATED: "Scénario créé avec succès",
            ERROR_CREATION: "Erreur lors de la création du scénario",
            MODIFIED: "Scénario modifié avec succès",
            ERROR_MODIFICATION: "Erreur lors de la modification du scénario",
        }
    },

    EASYCONNECT: {
        TITLE: "Easy Connect",
        REDIRECT: "connecter un appareil",
        DESCRIPTION: "connect un appareil à votre compte",
        MESSAGES: {
            CONNECT_DEVICE: "connecter un appareil",
            DEVICE_CODE: "code de l'appareil",
        },
        LOGS: {
            SPECIFY_CODE: "Veuillez spécifier un code d'appareil",
            INVALID_CREDENTIALS: "Mot de passe ou nom d'utilisateur incorrect",
            UNKNOWN_DEVICE: "code appareil inconnu",
            CONNECTED: "Appareil connecté avec succès",
        }
    },

    INVITE: {
        TITLE: "Inviter un utilisateur",
        REDIRECT: "Inviter",
        DESCRIPTION: "Envoyer un lien d'invitation à un futur utilisateur",
        MESSAGES: {
            GENERATE_INVITE: "Générer une invitation",
            VALIDATION_DELAY: "Cette invitation sera valide pendant 14 jours",
        },
        LOGS: {
            INVITE_SENT: "Invitation envoyée avec succès",
            INVITE_ERROR: "Erreur lors de l'envoi de l'invitation",
        }
    },

    PROFILE: {
        TITLE: "mon profile",
        REDIRECT: "mon profile",
        DESCRIPTION: "Voir et modifier mon profil",
        MESSAGES: {
            MODIFY_PASSWORD: "Modifier le mot de passe",
            OLD_PASSWORD: "Ancien mot de passe",
            NEW_PASSWORD: "Nouveau mot de passe",
        }
    },

    ADMIN: {
        TITLE: "administation",
        REDIRECT: "voir le panneau",
        DESCRIPTION: "voir et gérer l'application",
        MESSAGES: {
            SELECT_USER: "Sélectionner un utilisateur",
            CHANGE_ROLE: "Changer le rôle",
            REMOVE_USER: "Supprimer l'utilisateur",
            USER_SESSIONS: "Sessions de l'utilisateur",
        }
    },

    ABOUT: {
        TITLE: "A propos",
        REDIRECT: "Voir la page",
        DESCRIPTION: "Voir toutes les informations sur l'application",
        MESSAGES: {
            WITH_GRANDEST_SUPPORT: "Avec le support financier de la région Grand Est",
            INDICO_VERSION: "Indico - version {version}"
        }
    },

    FORGOTPASSWORD: {
        MESSAGES: {
            FORGOT_PASSWORD: "Mot de passe oublié",
            DESCRIPTION: "Apres avoir entré votre nom d'utilisateur ou email, vous recevrez les instructions pour réinitialiser votre mot de passe dans la boite mail associée à votre compte.",
        },
        LOGS: {
            SPECIFY_USERNAME_EMAIL: "Veuillez spécifier votre nom d'utilisateur ou votre email",
            INCORRECT_USERNAME_EMAIL: "Nom d'utilisateur ou email incorrect",
        }
    },
    
    REGISTER: {
        MESSAGES: {
            CONFIRM_PASSWORD: "Confirmer le mot de passe",
        },
        LOGS: {
            SPECIFY_FIRSTNAME: "Veuillez spécifier un prénom",
            SPECIFY_LASTNAME: "Veuillez spécifier un nom",
            SPECIFY_USERNAME: "Veuillez spécifier un nom d'utilisateur",
            SPECIFY_EMAIL: "Veuillez spécifier une adresse mail",
            SPECIFY_PASSWORD: "Veuillez spécifier un mot de passe d'au moins 8 caractères",
            SPECIFY_CONFIRM_PASSWORD: "Les deux mots de passe ne correspondent pas",
            CREATION_SUCCESS: "Compte créé avec succès",
            CREATION_ERROR: "Erreur pendante de création du compte",
            SERVER_ERROR: "Erreur lors de la communication avec le serveur",
            ERROR_MESSAGE: "Une erreur s'est produite",
        }
    },

    LOGIN: {
        LOGS: {
            INVALID_PASSWORD: "Mot de passe invalide",
            INVALID_USERNAME: "Nom d'utilisateur invalide",
        }
    },

    RESET: {
        MESSAGES: {
            TITLE: "{action} le mot de passe",
        },
        LOGS: {
            PASSWORD_RESET: "Mot de passe réinitialisé avec succès",
            TOKEN_ERROR: "token de réinitialisation invalide",
        }
    }
}

export default LANGUAGE;