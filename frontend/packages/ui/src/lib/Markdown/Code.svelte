<script lang="ts">
  import { highlight } from "./marked.js";

  export let source: string;
  let cls = "";
  export { cls as class };

  $: highlightedCode = highlight(source);
</script>

<pre class="{cls} w-full overflow-auto rounded-lg bg-[#292524] p-0 text-sm">
  <!-- eslint-disable svelte/no-at-html-tags --><code
    class="hljs language-javascript w-fit overflow-visible !bg-transparent !py-0"
    >{@html highlightedCode}
</code></pre>

<!--
  Eslint does currently not understand global css and complains,
  and as we have dynamic child nodes depending on the rendered code, we can currently not
  scope the css to only this component.
-->
<!-- eslint-disable svelte/valid-compile -->
<style global>
  pre code.hljs {
    display: block;
    overflow-x: auto;
    padding: 1em;
  }
  code.hljs {
    padding: 3px 5px;
  }
  .hljs {
    background: #2e3440;
  }
  .hljs,
  .hljs-subst {
    color: #d8dee9;
  }
  .hljs-selector-tag {
    color: #81a1c1;
  }
  .hljs-selector-id {
    color: #8fbcbb;
    font-weight: bold;
  }
  .hljs-selector-class {
    color: #8fbcbb;
  }
  .hljs-selector-attr {
    color: #8fbcbb;
  }
  .hljs-property {
    color: #88c0d0;
  }
  .hljs-selector-pseudo {
    color: #88c0d0;
  }
  .hljs-addition {
    background-color: rgba(163, 190, 140, 0.5);
  }
  .hljs-deletion {
    background-color: rgba(191, 97, 106, 0.5);
  }
  .hljs-built_in,
  .hljs-type {
    color: #8fbcbb;
  }
  .hljs-class {
    color: #8fbcbb;
  }
  .hljs-function {
    color: #88c0d0;
  }
  .hljs-title.hljs-function,
  .hljs-function > .hljs-title {
    color: #88c0d0;
  }
  .hljs-keyword,
  .hljs-literal,
  .hljs-symbol {
    color: #81a1c1;
  }
  .hljs-number {
    color: #b48ead;
  }
  .hljs-regexp {
    color: #ebcb8b;
  }
  .hljs-string {
    color: #a3be8c;
  }
  .hljs-title {
    color: #8fbcbb;
  }
  .hljs-params {
    color: #d8dee9;
  }
  .hljs-bullet {
    color: #81a1c1;
  }
  .hljs-code {
    color: #8fbcbb;
  }
  .hljs-emphasis {
    font-style: italic;
  }
  .hljs-formula {
    color: #8fbcbb;
  }
  .hljs-strong {
    font-weight: bold;
  }
  .hljs-link:hover {
    text-decoration: underline;
  }
  .hljs-quote {
    color: #4c566a;
  }
  .hljs-comment {
    color: #4c566a;
  }
  .hljs-doctag {
    color: #8fbcbb;
  }
  .hljs-meta,
  .hljs-meta .hljs-keyword {
    color: #5e81ac;
  }
  .hljs-meta .hljs-string {
    color: #a3be8c;
  }
  .hljs-attr {
    color: #8fbcbb;
  }
  .hljs-attribute {
    color: #d8dee9;
  }
  .hljs-name {
    color: #81a1c1;
  }
  .hljs-section {
    color: #88c0d0;
  }
  .hljs-tag {
    color: #81a1c1;
  }
  .hljs-variable {
    color: #d8dee9;
  }
  .hljs-template-variable {
    color: #d8dee9;
  }
  .hljs-template-tag {
    color: #5e81ac;
  }
</style>
