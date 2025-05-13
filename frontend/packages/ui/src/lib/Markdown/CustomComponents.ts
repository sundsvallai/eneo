/**
 * We have some custom components in our markdown syntax.
 */
import type { Component } from "svelte";

/**
 * 1. IntricInfoBlob
 */

export type IntricInrefToken = {
  type: "intricInref";
  level: "block" | "inline";
  raw: string;
  id: string;
};

export type IntricInrefCustomComponentProps = {
  /**
   * The generated token with the inref id and information about the tokens level (block or inline)
   */
  token: IntricInrefToken;
};

/**
 * Component that can be passed in to be rendered instead of the default component
 */
export type CustomInfoBlobComponent = Component<IntricInrefCustomComponentProps>;

/**
 * 2. IntricMention
 */
export type IntricMentionToken = {
  type: "intricMention";
  level: "inline";
  raw: string;
  handle: string;
};

export type IntricMentionCustomComponentProps = {
  /**
   * The generated token with the mention content
   */
  token: IntricMentionToken;
};

export type CustomMentionComponent = Component<IntricMentionCustomComponentProps>;

export type IntricToken = IntricInrefToken | IntricMentionToken;
export type CustomRenderers = {
  inref?: CustomInfoBlobComponent;
  mention?: CustomMentionComponent;
};
