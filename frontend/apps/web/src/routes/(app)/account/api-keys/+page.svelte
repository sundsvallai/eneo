<script lang="ts">
  import { invalidateAll } from "$app/navigation";
  import { Page } from "$lib/components/layout";
  import { getAppContext } from "$lib/core/AppContext.js";
  import { getIntric } from "$lib/core/Intric";
  import { Button, Dialog } from "@intric/ui";

  const {
    user,
    state: { userInfo }
  } = getAppContext();
  const intric = getIntric();

  let apiKey: string | null = null;
  let showCopiedMessage = false;

  async function generateApiKey() {
    apiKey = (await intric.users.generateApiKey()).key;
    invalidateAll();
  }
</script>

<svelte:head>
  <title>Intric.ai – Account – {$userInfo.firstName}</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="My API Keys"></Page.Title>
  </Page.Header>
  <Page.Main>
    <div
      class="border-default hover:bg-hover-dimmer flex items-center gap-1 border-b py-4 pr-4 pl-2"
    >
      <div class="flex flex-grow flex-col gap-1">
        <h3 class="font-medium">Api Key</h3>
        <pre class="">{apiKey
            ? apiKey
            : user.truncated_api_key
              ? `****${user.truncated_api_key}`
              : "No active key"}</pre>
      </div>
      {#if apiKey}
        <Button
          on:click={() => {
            if (!apiKey) {
              alert("No api key found. Please generate a new one.");
              return;
            }
            navigator.clipboard.writeText(apiKey);
            showCopiedMessage = true;
            setTimeout(() => {
              showCopiedMessage = false;
            }, 2000);
          }}
          variant="outlined"
          class="w-24"
        >
          <span>{showCopiedMessage ? "Copied!" : "Copy key"}</span>
        </Button>
      {/if}
      <Dialog.Root alert>
        <Dialog.Trigger asFragment let:trigger>
          <Button variant="outlined" is={trigger}>Generate API key</Button>
        </Dialog.Trigger>

        <Dialog.Content>
          <Dialog.Title>Generate new API key</Dialog.Title>
          <Dialog.Description
            >Do you really want to generate a new API key? <br /><br />Your old API key will get
            deleted in the process and no longer work.<br /><br /> Write down your new API key once it
            is generated, you will not be able to retrieve it from the server in the future.</Dialog.Description
          >

          <Dialog.Controls let:close>
            <Button is={close}>Cancel</Button>
            <Button is={close} variant="destructive" on:click={generateApiKey}
              >Generate new key</Button
            >
          </Dialog.Controls>
        </Dialog.Content>
      </Dialog.Root>
    </div>
  </Page.Main>
</Page.Root>
