<script lang="ts">
  import { browser } from "$app/environment";
  import { goto } from "$app/navigation";
  import { LoadingScreen } from "$lib/components/layout";

  export let data;

  if (browser) {
    if (data.zitadelLink) {
      window.location.href = data.zitadelLink;
    } else {
      goto("/login");
    }
  }
</script>

<LoadingScreen></LoadingScreen>
