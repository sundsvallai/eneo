<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->
<script lang="ts">
  import { Input, Tooltip } from "@intric/ui";

  export let kwargs: { temperature: number; top_p: number };
</script>

<div
  class="relative -mt-1 w-full border-y border-stone-300 bg-stone-50 px-4 py-4 hover:bg-stone-100"
>
  <h3 class="pb-1 pl-3 font-medium">Model configuration</h3>
  <div class="rounded-lg border border-stone-300 bg-white shadow">
    <div
      class="flex items-center gap-6 rounded-lg py-2 pl-3 pr-2 hover:bg-stone-50"
      aria-labelledby="temperature_label"
    >
      <Tooltip
        text={"Randomness: A value between 0 and 2 (Default: 1)\nHigher values will create more creative responses.\nLower values will be more deterministic."}
      >
        <p class="w-24" aria-label="Temperature setting" id="temperature_label">Temperature</p>
      </Tooltip>
      <Input.Slider bind:value={kwargs.temperature} max={2} min={0} step={0.01} />
      <Input.Number
        step={0.01}
        max={2}
        min={0}
        bind:value={kwargs.temperature}
        labelClass="hidden"
      />
    </div>
    <!-- For now we decided not to expose TOP P as a parameter to users -->
    <!-- <div class="border-b border-stone-200"></div>
    <div
      class="flex items-center gap-6 rounded-lg py-2 pl-3 pr-2 hover:bg-stone-50"
      aria-labelledby="top_p_setting"
    >
      <Tooltip
        text={"Diversity: A value between 0 and 1 (Default: 1)\nLower values restrict the number of potential completions the model can choose from."}
      >
        <p class="w-24" aria-label="Top P setting" id="top_p_label">Top P</p>
      </Tooltip>
      <Input.Slider bind:value={kwargs.top_p} max={1} min={0} step={0.01} />
      <Input.Number step={0.01} max={1} min={0} bind:value={kwargs.top_p} labelClass="hidden" />
    </div> -->
  </div>
</div>
