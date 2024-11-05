# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

# flake8: noqa
from instorage.roles.permissions import Permission

PERMISSIONS_WITH_DESCRIPTION = {
    Permission.ASSISTANTS: "Management of Assistants. Create, Update, and Delete Assistants.",
    Permission.SERVICES: "Management of Services. Create, Update, and Delete Services.",
    Permission.COLLECTIONS: "Management of Collections. Create, Update, and Delete Collections.",
    Permission.WEBSITES: "Management of Websites. Create, Update, and Delete Websites",
    Permission.INSIGHTS: "See Insights about your Organization.",
    Permission.AI: "More in-depth AI configuration.",
    Permission.EDITOR: "Edit any Assistant / Service / Collection that you have access to.",
    Permission.ADMIN: "Organization owner. Management of Users, Roles, and Groups.",
}
