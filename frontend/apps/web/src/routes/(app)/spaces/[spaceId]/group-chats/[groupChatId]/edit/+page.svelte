<script lang="ts">
  import { Page, Settings } from "$lib/components/layout";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager.js";
  import { Button, Input } from "@intric/ui";
  import { afterNavigate, beforeNavigate } from "$app/navigation";
  import { fade } from "svelte/transition";
  import { page } from "$app/state";
  import { initGroupChatEditor } from "$lib/features/group-chats/GroupChatEditor.js";
  import GroupChatAssistantList from "$lib/features/group-chats/components/GroupChatAssistantList.svelte";
  import PublishingSetting from "$lib/features/publishing/components/PublishingSetting.svelte";
  import { getChatQueryParams } from "$lib/features/chat/getChatQueryParams.js";

  export let data;

  const {
    state: { currentSpace },
    refreshCurrentSpace
  } = getSpacesManager();

  const {
    state: { resource, update, currentChanges, isSaving },
    saveChanges,
    discardChanges
  } = initGroupChatEditor({
    groupChat: data.groupChat,
    intric: data.intric,
    onUpdateDone() {
      refreshCurrentSpace("applications");
    }
  });

  beforeNavigate((navigate) => {
    if (
      $currentChanges.hasUnsavedChanges &&
      !confirm("You have unsaved changes. Do you want to discard all changes?")
    ) {
      navigate.cancel();
      return;
    }
    // Discard changes that have been made, this is only important so we delete uploaded
    // files that have not been saved to the assistant
    discardChanges();
  });

  let showSavesChangedNotice = false;

  // TODO
  let previousRoute = `/spaces/${$currentSpace.routeId}/chat/?${getChatQueryParams({ chatPartner: data.groupChat, tab: "chat" })}`;
  afterNavigate(({ from }) => {
    if (page.url.searchParams.get("next") === "default") return;
    if (from) previousRoute = from.url.toString();
  });
</script>

<svelte:head>
  <title
    >Eneo.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – {$resource.name}</title
  >
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title
      parent={{
        title: $resource.name,
        href: `/spaces/${$currentSpace.routeId}/chat/?${getChatQueryParams({ chatPartner: data.groupChat, tab: "chat" })}`
      }}
      title="Edit"
    ></Page.Title>

    <Page.Flex>
      {#if $currentChanges.hasUnsavedChanges}
        <Button
          variant="destructive"
          disabled={$isSaving}
          on:click={() => {
            discardChanges();
          }}>Discard all changes</Button
        >

        <Button
          variant="positive"
          class="w-32"
          on:click={async () => {
            await saveChanges();
            showSavesChangedNotice = true;
            setTimeout(() => {
              showSavesChangedNotice = false;
            }, 5000);
          }}>{$isSaving ? "Saving..." : "Save changes"}</Button
        >
      {:else}
        {#if showSavesChangedNotice}
          <p class="text-positive-stronger px-4" transition:fade>All changes saved!</p>
        {/if}
        <Button variant="primary" class="w-32" href={previousRoute}>Done</Button>
      {/if}
    </Page.Flex>
  </Page.Header>

  <Page.Main>
    <Settings.Page>
      <Settings.Group title="General">
        <Settings.Row
          title="Name"
          description="Give this group chat a name that will be displayed to its users."
          hasChanges={$currentChanges.diff.name !== undefined}
          revertFn={() => {
            discardChanges("name");
          }}
          let:aria
        >
          <input
            type="text"
            {...aria}
            bind:value={$update.name}
            class="border-default bg-primary ring-default rounded-lg border px-3 py-2 shadow focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
          />
        </Settings.Row>
      </Settings.Group>

      <Settings.Group title="Group settings">
        <Settings.Row
          title="Assistants"
          description="These assistants will be able to answer the users' questions. Intric uses the assistant's description to determine the most suitable assistant for each answer."
          hasChanges={$currentChanges.diff.tools?.assistants !== undefined}
          revertFn={() => {
            $update.tools.assistants = $resource.tools.assistants;
          }}
        >
          <GroupChatAssistantList bind:selectedAssistants={$update.tools.assistants} />
        </Settings.Row>
      </Settings.Group>

      <Settings.Group title="Advanced settings">
        <Settings.Row
          title="Mentions"
          description="Allow users to select which assistant should answer their question by mentioning them."
          hasChanges={$currentChanges.diff.allow_mentions !== undefined}
          revertFn={() => {
            discardChanges("allow_mentions");
          }}
        >
          <div class="border-default flex h-14 border-b py-2">
            <Input.RadioSwitch
              bind:value={$update.allow_mentions}
              labelTrue="Enable mentions"
              labelFalse="Disable mentions"
            ></Input.RadioSwitch>
          </div>
        </Settings.Row>

        <Settings.Row
          title="Response labels"
          description="Show the answering assistant's name next to its response during a chat."
          hasChanges={$currentChanges.diff.show_response_label !== undefined}
          revertFn={() => {
            discardChanges("show_response_label");
          }}
        >
          <div class="border-default flex h-14 border-b py-2">
            <Input.RadioSwitch
              bind:value={$update.show_response_label}
              labelTrue="Show labels"
              labelFalse="Hide labels"
            ></Input.RadioSwitch>
          </div>
        </Settings.Row>
      </Settings.Group>

      {#if data.groupChat.permissions?.some((permission) => permission === "insight_toggle" || permission === "publish")}
        <Settings.Group title="Publishing">
          {#if data.groupChat.permissions?.includes("publish")}
            <Settings.Row
              title="Status"
              description="Publishing your assistant will make it available to all users of this space, including viewers."
            >
              <PublishingSetting
                endpoints={data.intric.groupChats}
                resource={data.groupChat}
                hasUnsavedChanges={$currentChanges.hasUnsavedChanges}
              />
            </Settings.Row>
          {/if}

          {#if data.groupChat.permissions?.includes("insight_toggle")}
            <Settings.Row
              hasChanges={$currentChanges.diff.insight_enabled !== undefined}
              revertFn={() => {
                discardChanges("insight_enabled");
              }}
              title="Insights"
              description="Collect insights about this assistant's usage and let space editors/admins view a complete history of all user questions."
            >
              <div class="border-default flex h-14 border-b py-2">
                <Input.RadioSwitch
                  bind:value={$update.insight_enabled}
                  labelTrue="Enable insights"
                  labelFalse="Disable insights"
                ></Input.RadioSwitch>
              </div>
            </Settings.Row>
          {/if}
        </Settings.Group>
      {/if}

      <div class="min-h-24"></div>
    </Settings.Page>
  </Page.Main>
</Page.Root>
