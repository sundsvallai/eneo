<script lang="ts">
  import { browser } from "$app/environment";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  if ($page.error?.sessionInvalid && browser) {
    goto("/logout");
  }
</script>

<div class="flex h-[100svh] w-screen flex-col items-center justify-center gap-1">
  <div class="text-2xl">{$page.error?.status}: {$page.error?.message}</div>
  <p>We're experiencing some difficulties, please try again later.</p>
</div>
