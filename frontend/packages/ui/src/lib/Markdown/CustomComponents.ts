/**
 * We have some custom components in our markdown syntax.
 */

import type { InfoBlob } from "@intric/intric-js";
import type { ComponentType, SvelteComponent } from "svelte";

/**
 * 1. IntricInfoBlob
 */

export type IntricInrefToken = {
  type: "intricInref";
  raw: string;
  id: string;
};

/**
 * Component that can be passed in to be rendered instead of the default component
 */
export type CustomInfoBlobComponent = ComponentType<
  SvelteComponent<{
    /**
     * The id specified by the custom ref component, usually the start of the InfoBlobs UUID
     * Use it to find the actual reference in the references with reference.id.startsWith(id)
     * */
    id: string;
    /** A list of all available references in a message */
    references: InfoBlob[];
  }>
>;

export type IntricToken = IntricInrefToken;
export type CustomRenderers = {
  inref?: {
    references?: InfoBlob[];
    component?: CustomInfoBlobComponent;
  };
};
