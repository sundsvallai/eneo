<script lang="ts">
  import { Page } from "$lib/components/layout";
  import SelectTheme from "$lib/components/SelectTheme.svelte";
  import { getAppContext } from "$lib/core/AppContext.js";
  import UpdateUserName from "./UpdateUserName.svelte";
  const {
    user,
    versions,
    featureFlags,
    state: { userInfo }
  } = getAppContext();
</script>

<svelte:head>
  <title>Eneo.ai – Account – {$userInfo.firstName}</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Account"></Page.Title>
  </Page.Header>
  <Page.Main>
    {#if featureFlags.newAuth}
      <div
        class="border-dimmer hover:bg-hover-dimmer flex items-center gap-12 border-b py-4 pl-2 pr-4"
      >
        <div class="flex flex-col gap-1">
          <h3 class="font-medium">First Name</h3>
          <pre class="">{$userInfo.firstName}</pre>
        </div>
        <div class="flex flex-col gap-1">
          <h3 class="font-medium">Last Name</h3>
          <pre class="">{$userInfo.lastName}</pre>
        </div>
        <div class="flex flex-col gap-1">
          <h3 class="font-medium">Full Name</h3>
          <pre class="">{$userInfo.displayName}</pre>
        </div>
        <!-- Changing name only supported for username/password users -->
        {#if !$userInfo.usesIdp}
          <div class="flex-grow"></div>
          <UpdateUserName
            firstName={$userInfo.firstName}
            lastName={$userInfo.lastName}
            displayName={$userInfo.displayName}
          ></UpdateUserName>
        {/if}
      </div>
    {:else}
      <div class="border-dimmer hover:bg-hover-dimmer flex flex-col gap-1 border-b py-4 pl-2 pr-4">
        <h3 class="font-medium">Username</h3>
        <pre class="">{user.username}</pre>
      </div>
    {/if}
    <div class="border-dimmer hover:bg-hover-dimmer flex flex-col gap-1 border-b py-4 pl-2 pr-4">
      <h3 class="font-medium">Email</h3>
      <pre class="">{user.email}</pre>
    </div>
    <div
      class="border-dimmer hover:bg-hover-dimmer flex flex-col gap-2 border-b pb-2 pl-2 pr-4 pt-4"
    >
      <span class="font-medium" aria-hidden="true">Colour scheme</span>
      <SelectTheme></SelectTheme>
    </div>
    <div class="border-dimmer hover:bg-hover-dimmer flex flex-col gap-1 border-b py-4 pl-2 pr-4">
      <h3 class="font-medium">Versions</h3>
      <pre
        class="">Frontend: {versions.frontend} · Client: {versions.client} · Backend: {versions.backend}</pre>
    </div>
    {#if versions.preview}
      <div class="border-dimmer hover:bg-hover-dimmer flex flex-col gap-1 border-b py-4 pl-2 pr-4">
        <h3 class="font-medium">Preview</h3>
        <pre class="">Branch: {versions.preview.branch}<br />Commit: {versions.preview.commit}</pre>
      </div>
    {/if}
  </Page.Main>
</Page.Root>
