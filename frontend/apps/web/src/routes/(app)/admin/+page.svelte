<!-- MIT License -->

<script lang="ts">
  import { Page } from "$lib/components/layout/index.js";
  import { getAppContext } from "$lib/core/AppContext.js";

  function formatBytes(bytes: number, decimals = 2) {
    if (!+bytes) return "0 Bytes";

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
  }

  const { tenant } = getAppContext();
</script>

<svelte:head>
  <title>Intric.ai - {tenant.display_name}</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title>Organisation</Page.Title>
  </Page.Header>
  <Page.Main>
    <div class="flex flex-col gap-1 border-b border-stone-100 py-4 pl-2 pr-4 hover:bg-stone-50">
      <h3 class="font-medium">Quota limit</h3>
      <pre class="">{formatBytes(tenant.quota_limit ?? 0)}</pre>
    </div>
  </Page.Main>
</Page.Root>
