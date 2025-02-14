<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { Button, Input } from "@intric/ui";
  import { getIntric } from "$lib/core/Intric";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import EditService from "./EditService.svelte";
  import { dynamicColour } from "$lib/core/colours";

  const intric = getIntric();
  const {
    state: { currentSpace }
  } = getSpacesManager();

  export let data;

  let playgroundInput = "";
  let playgroundOutput = "";
  let runningService = false;

  async function runService() {
    runningService = true;
    try {
      const result = await intric.services.run({ service: data.service, input: playgroundInput });
      if (typeof result === "string") {
        playgroundOutput = result;
      } else {
        playgroundOutput = JSON.stringify(result);
      }
    } catch (e) {
      console.error(e);
      playgroundOutput = JSON.stringify(e);
    }
    runningService = false;
  }
</script>

<svelte:head>
  <title
    >Intric.ai – {$currentSpace.personal ? "Personal" : $currentSpace.name} - {data.service
      .name}</title
  >
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title
      parent={{ title: "Services", href: `/spaces/${$currentSpace.routeId}/services` }}
      title={data.service.name}
    ></Page.Title>
  </Page.Header>

  <Page.LegacyTabbar>
    <Page.Flex>
      <Page.LegacyTabTrigger tab="playground" label="Test your service {data.service.name}"
        >Playground</Page.LegacyTabTrigger
      >
    </Page.Flex>
    <Page.Flex>
      <Page.LegacyTabTrigger tab="edit">Settings</Page.LegacyTabTrigger>
    </Page.Flex>
  </Page.LegacyTabbar>

  <Page.Main>
    <Page.Tab id="playground">
      <div
        {...dynamicColour({ basedOn: data.service.id })}
        class="grid h-full grid-cols-1 gap-4 py-4 pr-4 md:grid-cols-2"
      >
        <div class="flex h-full flex-col items-end gap-4">
          <Input.TextArea bind:value={playgroundInput} label="Input" class="h-full w-full"
          ></Input.TextArea>
          <Button variant="primary" on:click={runService}>
            {#if runningService}Running...{:else}
              Run this service{/if}</Button
          >
        </div>
        <div class="flex flex-col items-end gap-1">
          <h3 class="self-start font-medium">Output</h3>
          <div
            class="h-full w-full overflow-y-auto border-b border-dynamic-default bg-dynamic-dimmer p-4 font-mono text-sm text-dynamic-default"
          >
            {runningService ? "Loading..." : playgroundOutput}
          </div>

          <Button
            variant="primary"
            class="mt-3"
            on:click={() => {
              navigator.clipboard.writeText(playgroundOutput);
            }}>Copy response</Button
          >
        </div>
      </div>
    </Page.Tab>
    <Page.Tab id="edit">
      <EditService service={data.service}></EditService>
    </Page.Tab>
  </Page.Main>
</Page.Root>
