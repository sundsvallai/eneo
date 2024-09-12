<!-- MIT License -->

<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import { Button } from "@intric/ui";
  import MembersList from "./members/MembersList.svelte";
  import { getAppContext } from "$lib/core/AppContext";
  import { Page } from "$lib/components/layout";

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const { user } = getAppContext();
</script>

<svelte:head>
  <title>Intric.ai – {$currentSpace.personal ? "Personal" : $currentSpace.name} – Overview</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title>Overview</Page.Title>
    <MembersList></MembersList>
  </Page.Header>

  <Page.Main>
    <div class="flex flex-grow flex-col overflow-y-auto pl-2 pr-4 pt-4">
      <div class="flex items-center justify-start gap-4 pb-4">
        <h1 class="text-[2rem] font-bold">
          {$currentSpace.personal ? `Hi, ${user.username}!` : $currentSpace.name}
        </h1>
      </div>
      {#if $currentSpace.personal}
        <p class="min-h-20 max-w-[70ch]">
          You can build and experiment with your own AI applications in your personal space.
        </p>
      {:else}
        <p class="min-h-20">{$currentSpace.description ?? `Welcome to ${$currentSpace.name}`}</p>
      {/if}
      <!-- <div class="flex-grow"></div> -->

      <div class="grid aspect-square grid-cols-1 gap-4 pb-4 pt-4 md:grid-cols-2">
        {#if $currentSpace.hasPermission("read", "assistant")}
          <Button
            unstyled
            href="/spaces/{$currentSpace.routeId}/assistants"
            class="flex cursor-pointer flex-col border-t border-black/10 bg-stone-50 px-4 py-2 hover:bg-stone-100"
          >
            <h3 class="font-mono text-sm uppercase">Assistants</h3>
            <div class="flex-grow"></div>
            <div class="self-end text-[4rem] font-bold">
              {$currentSpace.applications.assistants.length}
            </div>
          </Button>
        {/if}
        {#if $currentSpace.hasPermission("read", "service")}
          <Button
            unstyled
            href="/spaces/{$currentSpace.routeId}/services"
            class="flex cursor-pointer flex-col border-t border-black/10 bg-stone-50 px-4 py-2 hover:bg-stone-100"
          >
            <h3 class="font-mono text-sm uppercase">Services</h3>
            <div class="flex-grow"></div>
            <div class="self-end text-[4rem] font-bold">
              {$currentSpace.applications.services.length}
            </div>
          </Button>
        {/if}
        {#if $currentSpace.hasPermission("read", "collection")}
          <Button
            unstyled
            href="/spaces/{$currentSpace.routeId}/knowledge?tab=collections"
            class="flex cursor-pointer flex-col border-t border-black/10 bg-stone-50 px-4 py-2 hover:bg-stone-100"
          >
            <h3 class="font-mono text-sm uppercase">Collections</h3>
            <div class="flex-grow"></div>

            <div class="self-end text-[4rem] font-bold">
              {$currentSpace.knowledge.groups.length}
            </div>
          </Button>
        {/if}
        {#if $currentSpace.hasPermission("read", "website")}
          <Button
            unstyled
            href="/spaces/{$currentSpace.routeId}/knowledge?tab=websites"
            class="flex cursor-pointer flex-col border-t border-black/10 bg-stone-50 px-4 py-2 hover:bg-stone-100"
          >
            <h3 class="font-mono text-sm uppercase">Websites</h3>
            <div class="flex-grow"></div>

            <div class="self-end text-[4rem] font-bold">
              {$currentSpace.knowledge.websites.length}
            </div>
          </Button>
        {/if}
        {#if $currentSpace.hasPermission("read", "member")}
          <Button
            unstyled
            href="/spaces/{$currentSpace.routeId}/members"
            class="flex cursor-pointer flex-col border-t border-black/10 bg-stone-50 px-4 py-2 hover:bg-stone-100"
          >
            <h3 class="font-mono text-sm uppercase">Members</h3>
            <div class="flex-grow"></div>

            <div class="self-end text-[4rem] font-bold">
              {$currentSpace.members.length}
            </div>
          </Button>
        {/if}
      </div>
    </div>
  </Page.Main>
</Page.Root>
