// See https://kit.svelte.dev/docs/types#app

import type { AssistantSession } from "@intric/intric-js";

// for information about these interfaces
declare global {
  namespace App {
    interface Error {
      message: string;
      status: number;
      sessionInvalid: boolean;
    }
    interface Locals {
      user:
        | {
            isLoggedIn: true;
            token: string;
          }
        | { isLoggedIn: false };
    }
    interface PageData {}
    interface PageState {
      currentSpace?: Space;
      session?: AssistantSession;
      tab?: string;
    }
    // interface Platform {}
  }

  // App version
  declare const __FRONTEND_VERSION__: string;
  declare const __VERCEL_ENV__: string | undefined;
  declare const __GIT_BRANCH__: string | undefined;
  declare const __GIT_COMMIT_SHA__: string | undefined;

  // View transition API
  interface ViewTransition {
    updateCallbackDone: Promise<void>;
    ready: Promise<void>;
    finished: Promise<void>;
    skipTransition: () => void;
  }

  interface Document {
    startViewTransition(updateCallback: () => Promise<void>): ViewTransition;
  }

  interface CSSStyleDeclaration {
    viewTransitionName: string;
  }
}

export {};
