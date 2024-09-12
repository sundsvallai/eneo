<script lang="ts">
  import type { InfoBlob } from "@intric/intric-js";
  import { Button } from "@intric/ui";
  export let blob: InfoBlob;
</script>

<Button
  href={blob.metadata.url ?? ""}
  target="_blank"
  variant="simple"
  class="max-w-[30ch] bg-white text-blue-600 shadow-sm visited:text-purple-600 hover:text-blue-800"
>
  <span class="truncate underline">
    {blob.metadata.url}
  </span>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="1.5"
    stroke="currentColor"
    class="h-6 w-6 min-w-6 text-stone-400"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25"
    />
  </svg>
</Button>
