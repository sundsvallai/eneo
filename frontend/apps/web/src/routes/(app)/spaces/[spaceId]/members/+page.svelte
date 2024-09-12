<!-- MIT License -->

<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import MemberChip from "./MemberChip.svelte";
  import AddMember from "./AddMember.svelte";
  import MemberRole from "./MemberRole.svelte";
  import { Page } from "$lib/components/layout";

  export let data;

  const { user } = getAppContext();

  const {
    state: { currentSpace }
  } = getSpacesManager();
</script>

<svelte:head>
  <title>Intric.ai – {$currentSpace.name} – Members</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title>Members</Page.Title>
    {#if $currentSpace.hasPermission("add", "member")}
      <AddMember allUsers={data.users} currentMembers={$currentSpace.members}></AddMember>
    {/if}
  </Page.Header>
  <Page.Main>
    <div class="flex flex-col gap-4 py-5 pr-6 lg:flex-row lg:gap-12">
      <div class="pl-2 lg:w-2/5">
        <h3 class="pb-1 text-lg font-medium">Admins & Editors</h3>
        <p class="text-stone-500">
          People that can open and edit this space, including creating new assistants and uploading
          knowledge.
        </p>
      </div>

      <div class="flex flex-grow flex-col">
        {#each $currentSpace.members as member}
          <div
            class="flex items-center justify-between gap-4 border-b border-black/10 py-4 pl-4 pr-4 hover:bg-stone-50"
          >
            <MemberChip {member}></MemberChip>
            {#if user.id === member.id}
              {member.username} <span class="text-stone-500">(you)</span>
            {:else}
              {member.username}
            {/if}
            <div class="flex-grow"></div>
            {#if $currentSpace.hasPermission("edit", "member") && user.id !== member.id}
              <MemberRole {member}></MemberRole>
            {:else}
              <span class="px-2 capitalize text-stone-500">{member.role}</span>
            {/if}
          </div>
        {/each}
      </div>
    </div>

    <div class="flex flex-col gap-4 py-5 pr-6 lg:flex-row lg:gap-12">
      <div class="pl-2 lg:w-2/5">
        <h3 class="pb-1 text-lg font-medium">Viewers</h3>
        <p class="text-stone-500">
          People that can see and interact with this space's published assistants in their
          Dashboard.
        </p>
      </div>

      <div class="flex flex-grow flex-col">
        <div
          class="flex items-center justify-between border-b border-black/10 py-4 pl-2 pr-4 hover:bg-stone-50"
        >
          Coming soon...
        </div>
      </div>
    </div>
  </Page.Main>
</Page.Root>
