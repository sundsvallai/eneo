<script lang="ts">
  import {
    behaviourList,
    getBehaviour,
    getKwargs,
    type ModelBehaviour,
    type ModelKwArgs
  } from "../ModelBehaviours";
  import { createSelect } from "@melt-ui/svelte";
  import { IconChevronDown } from "@intric/icons/chevron-down";
  import { IconCheck } from "@intric/icons/check";
  import { IconQuestionMark } from "@intric/icons/question-mark";
  import { Input, Tooltip } from "@intric/ui";

  export let kwArgs: ModelKwArgs;

  export let aria: AriaProps = { "aria-label": "Select model behaviour" };

  const {
    elements: { trigger, menu, option },
    helpers: { isSelected },
    states: { selected }
  } = createSelect<ModelBehaviour>({
    defaultSelected: { value: getBehaviour(kwArgs) },
    positioning: {
      placement: "bottom",
      fitViewport: true,
      sameWidth: true
    },
    portal: null,
    onSelectedChange: ({ next }) => {
      const args = next?.value ? getKwargs(next.value) : getKwargs("default");
      // If the user selects "custom", we want to keep the current kwargs settings if they already are custom
      // However, if they are not, then we initialise with a default custom setting
      const customArgs =
        getBehaviour(kwArgs) === "custom" ? kwArgs : { temperature: 1, top_p: null };
      // keep in mind: setting the kwargs will trigger the `watchKwArgs` function
      kwArgs = args ? args : customArgs;
      return next;
    }
  });

  // This function will only be called on direct user input of custom temperature
  // If the selected value is not a named value, it will set the Kwargs
  // This can't be a declarative statement with $: as it would fire in too many situations
  let customTemp: number = 1;
  function maybeSetKwArgsCustom() {
    const args = { temperature: customTemp, top_p: null };
    if (getBehaviour(args) === "custom") {
      kwArgs = args;
    }
  }

  function watchChanges(currentKwArgs: ModelKwArgs) {
    const behaviour = getBehaviour(currentKwArgs);

    if ($selected?.value !== behaviour) {
      $selected = { value: behaviour };
    }

    if (
      behaviour === "custom" &&
      currentKwArgs.temperature &&
      currentKwArgs.temperature !== customTemp
    ) {
      customTemp = currentKwArgs.temperature;
    }
  }

  $: watchChanges(kwArgs);
</script>

<button
  {...$trigger}
  {...aria}
  use:trigger
  class="flex h-16 items-center justify-between border-b border-default px-4 hover:bg-hover-default"
>
  <span class="capitalize">{$selected?.value ?? "No behaviour found"}</span>
  <IconChevronDown />
</button>

<div
  class="z-20 flex flex-col overflow-y-auto rounded-lg border border-stronger bg-primary shadow-xl"
  {...$menu}
  use:menu
>
  <div
    class="bg-frosted-glass-secondary sticky top-0 border-b border-default px-4 py-2 font-mono text-sm"
  >
    Select a model behaviour
  </div>
  {#each behaviourList as behavior}
    <div
      class="flex min-h-16 items-center justify-between border-b border-default px-4 hover:cursor-pointer hover:bg-hover-stronger"
      {...$option({ value: behavior })}
      use:option
    >
      <span class="capitalize">
        {behavior}
      </span>
      <div class="check {$isSelected(behavior) ? 'block' : 'hidden'}">
        <IconCheck class="text-positive-default" />
      </div>
    </div>
  {/each}
</div>

{#if $selected?.value === "custom"}
  <div
    class="flex h-[4.125rem] items-center justify-between gap-8 border-b border-default px-4 hover:bg-hover-stronger"
  >
    <div class="flex items-center gap-2">
      <p class="w-24" aria-label="Temperature setting" id="temperature_label">Temperature</p>
      <Tooltip
        text={"Randomness: A value between 0 and 2 (Default: 1)\nHigher values will create more creative responses.\nLower values will be more deterministic."}
      >
        <IconQuestionMark class="text-muted hover:text-primary" />
      </Tooltip>
    </div>
    <Input.Slider
      bind:value={customTemp}
      max={2}
      min={0}
      step={0.01}
      onInput={maybeSetKwArgsCustom}
    />
    <Input.Number
      onInput={maybeSetKwArgsCustom}
      bind:value={customTemp}
      step={0.01}
      max={2}
      min={0}
      hiddenLabel={true}
    ></Input.Number>
  </div>
{/if}

<style lang="postcss">
  div[data-highlighted] {
    @apply bg-hover-default;
  }

  /* div[data-selected] { } */

  div[data-disabled] {
    @apply opacity-30 hover:bg-transparent;
  }
</style>
