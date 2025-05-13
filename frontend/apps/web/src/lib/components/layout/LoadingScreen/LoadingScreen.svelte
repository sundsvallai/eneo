<script lang="ts">
  import IntricWordMark from "$lib/assets/IntricWordMark.svelte";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
</script>

<div class="absolute inset-0 flex flex-col items-center justify-center gap-4">
  <IntricWordMark class="text-brand-intric h-8 w-20"></IntricWordMark>
  <IconLoadingSpinner class="animate-spin" />
</div>
