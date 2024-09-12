<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { getAppContext } from "$lib/core/AppContext.js";
  const { user, versions } = getAppContext();
</script>

<svelte:head>
  <title>Intric.ai – Account – {user.username}</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title>Account</Page.Title>
  </Page.Header>
  <Page.Main>
    <div class="flex flex-col gap-1 border-b border-stone-100 py-4 pl-2 pr-4 hover:bg-stone-50">
      <h3 class="font-medium">Username</h3>
      <pre class="">{user.username}</pre>
    </div>
    <div class="flex flex-col gap-1 border-b border-stone-100 py-4 pl-2 pr-4 hover:bg-stone-50">
      <h3 class="font-medium">Email</h3>
      <pre class="">{user.email}</pre>
    </div>
    <div class="flex flex-col gap-1 border-b border-stone-100 py-4 pl-2 pr-4 hover:bg-stone-50">
      <h3 class="font-medium">Versions</h3>
      <pre
        class="">Frontend: {versions.frontend} · Client: {versions.client} · Backend: {versions.backend}</pre>
    </div>
    {#if versions.preview}
      <div class="flex flex-col gap-1 border-b border-stone-100 py-4 pl-2 pr-4 hover:bg-stone-50">
        <h3 class="font-medium">Preview</h3>
        <pre class="">Branch: {versions.preview.branch}<br />Commit: {versions.preview.commit}</pre>
      </div>
    {/if}
  </Page.Main>
</Page.Root>
