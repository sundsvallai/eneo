<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { dynamicColour } from "$lib/core/colours";
  import MemberChip from "$lib/features/spaces/components/MemberChip.svelte";
  import AccountMenu from "./AccountMenu.svelte";
  const { user } = getAppContext();
</script>

<div
  class="absolute inset-0 flex flex-grow justify-stretch"
  {...dynamicColour({ basedOn: user.email })}
>
  <div class="flex flex-col border-r-[0.5px] border-default md:min-w-[17rem] md:max-w-[17rem]">
    <div
      class="group relative flex h-[4.25rem] w-full items-center justify-start gap-3 border-b-[0.5px] border-default pl-[1.4rem] pr-5 pt-0.5 font-medium"
    >
      <div class="-ml-[0.48rem]"></div>
      <MemberChip member={user}></MemberChip>
      <span class="flex-grow truncate pl-0.5 text-left text-primary"> {user.email} </span>
    </div>
    <AccountMenu></AccountMenu>
  </div>
  <slot />
  <div
    class="pointer-events-none absolute inset-0 -z-0 flex flex-grow shadow-xl md:left-[17rem]"
  ></div>
</div>
