import type { MarkedToken } from "marked";
import type { ComponentType } from "svelte";
import type { IntricToken } from "../CustomComponents";
import Heading from "./Heading.svelte";
import Text from "./Text.svelte";
import Paragraph from "./Paragraph.svelte";
import List from "./List.svelte";
import ListItem from "./ListItem.svelte";
import Strong from "./Strong.svelte";
import Emphasis from "./Emphasis.svelte";
import Code from "./Code.svelte";
import Inref from "./Inref.svelte";
import CodeSpan from "./CodeSpan.svelte";
import Blockquote from "./Blockquote.svelte";
import Del from "./Del.svelte";
import Br from "./Br.svelte";
import Hr from "./Hr.svelte";
import Space from "./Space.svelte";
import Def from "./Def.svelte";
import Table from "./Table.svelte";
import Link from "./Link.svelte";
import Image from "./Image.svelte";

export const renderers: Record<MarkedToken["type"] | IntricToken["type"], ComponentType> = {
  // Custom blocks
  intricInref: Inref,
  // Basic markdown blocks
  heading: Heading,
  text: Text,
  paragraph: Paragraph,
  list: List,
  list_item: ListItem,
  strong: Strong,
  em: Emphasis,
  code: Code,
  codespan: CodeSpan,
  blockquote: Blockquote,
  del: Del,
  br: Br,
  hr: Hr,
  space: Space,
  def: Def,
  escape: Space,
  table: Table,
  link: Link,
  image: Image,
  html: CodeSpan // We're not rendering any html tags
};

export type SupportedTokenType = keyof typeof renderers;

export function isSupportedToken(tokenType: string): tokenType is SupportedTokenType {
  return tokenType in renderers;
}
