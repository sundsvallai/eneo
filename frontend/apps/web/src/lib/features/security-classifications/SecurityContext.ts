/*
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
*/

import { createContext } from "$lib/core/context";
import type { Intric } from "@intric/intric-js";

type SecurityContext = Awaited<ReturnType<Intric["securityClassifications"]["list"]>>;

export const [getSecurityContext, setSecurityContext] = createContext<SecurityContext>("security");
