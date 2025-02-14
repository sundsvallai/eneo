<script>
  import { Markdown } from "$lib";
  let source = "";

  let debug = false;
</script>

<div class="absolute inset-0 grid grid-cols-2 items-center justify-center gap-4 p-8">
  <div class="h-full overflow-y-auto rounded border p-4">
    <pre contenteditable="true" bind:innerText={source}></pre>
  </div>
  <div class="h-full overflow-y-auto rounded border p-4">
    <button
      class="absolute right-2 top-2 bg-secondary px-2 py-1 hover:bg-hover-stronger"
      on:click={() => {
        debug = !debug;
      }}>({debug ? "Debug (On)" : "Debug (Off)"})</button
    >
    <Markdown {source} showTokenOutput={debug}></Markdown>
  </div>
</div>
