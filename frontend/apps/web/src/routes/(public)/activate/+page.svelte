<script lang="ts">
  import IntricWordMark from "$lib/assets/IntricWordMark.svelte";
  import { Button } from "@intric/ui";
</script>

<div class="absolute inset-0 flex flex-col items-center justify-center gap-4">
  <div class=" flex flex-col items-start rounded-sm border border-default bg-primary p-8 shadow">
    <IntricWordMark class="h-8 w-16 text-brand-intric" />
    <div class="h-14"></div>
    <h2 class="mb-2 text-2xl font-bold">Almost there!</h2>
    <p class="max-w-[60ch] text-secondary">
      Your account has not yet been activated in intric. Please ask your administrator to create an
      invitation for your email address and then try again.
    </p>
    <div class="h-16"></div>

    <div class="flex w-full justify-between">
      <Button href="/logout" variant="outlined">Logout</Button>
      <Button href="/" variant="primary">Retry</Button>
    </div>
  </div>
</div>
