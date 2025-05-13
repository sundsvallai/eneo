<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Select } from "@intric/ui";
  import { behaviourList, type ModelBehaviour } from "../ModelBehaviours";

  export let value: ModelBehaviour;

  const behaviourLabels: Record<ModelBehaviour, string> = {
    creative: "Creative",
    default: "Default",
    deterministic: "Deterministic",
    custom: "Custom"
  };
</script>

<Select.Simple
  class="border-dimmer hover:bg-hover-dimmer relative w-full border-b px-4 py-4"
  bind:value
  options={behaviourList.map((behaviour) => ({
    value: behaviour,
    label: behaviourLabels[behaviour]
  }))}>Model behaviour</Select.Simple
>
