<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import MemberChip from "$lib/features/spaces/components/MemberChip.svelte";
  import AddMember from "./AddMember.svelte";
  import MemberRole from "./MemberRole.svelte";
  import { Page, Settings } from "$lib/components/layout";

  const { user } = getAppContext();

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const isViewerRoleAvailable = $currentSpace.available_roles.some(
    (role) => role.value === "viewer"
  );

  $: editors = $currentSpace.members.filter(
    (member) => member.role === "admin" || member.role === "editor"
  );

  $: viewers = $currentSpace.members.filter((member) => member.role === "viewer");
</script>

<svelte:head>
  <title>Intric.ai – {$currentSpace.name} – Members</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Members"></Page.Title>
    {#if $currentSpace.hasPermission("add", "member")}
      <AddMember></AddMember>
    {/if}
  </Page.Header>
  <Page.Main>
    <Settings.Page>
      <Settings.Group title="Current members">
        <Settings.Row
          title="Admins & Editors"
          description="People that can create and edit new assistants and apps, and manage this space's knowledge."
        >
          <div class="flex flex-grow flex-col">
            {#each editors as member (member.id)}
              <div
                class="border-default hover:bg-hover-dimmer flex items-center justify-between gap-4 border-b py-4 pr-4 pl-4"
              >
                <MemberChip {member}></MemberChip>
                {#if user.id === member.id}
                  <span class="text-primary">{member.email} (you)</span>
                {:else}
                  <span class="text-primary">{member.email}</span>
                {/if}
                <div class="flex-grow"></div>
                {#if $currentSpace.hasPermission("edit", "member") && user.id !== member.id}
                  <MemberRole {member}></MemberRole>
                {:else}
                  <span class="text-secondary px-2 capitalize">{member.role}</span>
                {/if}
              </div>
            {/each}
          </div>
        </Settings.Row>

        {#if isViewerRoleAvailable}
          <Settings.Row
            title="Viewers"
            description="People that can see and use this space's published assistants and apps."
          >
            <div class="flex flex-grow flex-col">
              {#if viewers.length > 0}
                {#each viewers as member (member.id)}
                  <div
                    class="border-default hover:bg-hover-dimmer flex items-center justify-between gap-4 border-b py-4 pr-4 pl-4"
                  >
                    <MemberChip {member}></MemberChip>
                    {#if user.id === member.id}
                      <span class="text-primary">{member.email} (you)</span>
                    {:else}
                      <span class="text-primary">{member.email}</span>
                    {/if}
                    <div class="flex-grow"></div>
                    {#if $currentSpace.hasPermission("edit", "member") && user.id !== member.id}
                      <MemberRole {member}></MemberRole>
                    {:else}
                      <span class="text-secondary px-2 capitalize">{member.role}</span>
                    {/if}
                  </div>
                {/each}
              {:else}
                <div
                  class="border-default text-muted hover:bg-hover-dimmer flex items-center justify-between gap-4 border-b py-4 pr-4 pl-4"
                >
                  There are currently no viewers in this space
                </div>
              {/if}
            </div>
          </Settings.Row>
        {/if}
      </Settings.Group>
    </Settings.Page>
  </Page.Main>
</Page.Root>
