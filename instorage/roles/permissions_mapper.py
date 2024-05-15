# MIT License

# flake8: noqa
from instorage.roles.permissions import Permission

PERMISSIONS_WITH_DESCRIPTION = {
    Permission.ASSISTANTS: "Management of Assistants. Create, Update, and Delete Assistants.",
    Permission.SERVICES: "Management of Services. Create, Update, and Delete Services.",
    Permission.COLLECTIONS: "Management of Collections. Create, Update, and Delete Collections.",
    Permission.INSIGHTS: "See Insights about your Organization.",
    Permission.AI: "More in-depth AI configuration.",
    Permission.COMPLIANCE: "Manage Compliance configurations.",
    Permission.DEPLOYER: "Deploy Assistants / Services / Collections as Widgets, and to any User Group.",
    Permission.EDITOR: "Edit any Assistant / Service / Collection that you have access to.",
    Permission.ADMIN: "Organization owner. Management of Users, Roles, and Groups.",
}
