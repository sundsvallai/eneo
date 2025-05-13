<script lang="ts">
  import { Select } from "@intric/ui";
  import { availableThemes, type Theme } from "../core/theme";
  import { getThemeStore } from "../core/theme";
  import { writable } from "svelte/store";
  const currentTheme = getThemeStore();
  function capitalise(string: string) {
    const first = [...string][0].toUpperCase();
    return first + string.substring(1);
  }
  const selected = writable<{ label: string; value: Theme }>({
    label: capitalise($currentTheme),
    value: $currentTheme
  });
  $: $currentTheme = $selected.value;
</script>

<Select.Root customStore={selected}>
  <div class="sr-only">
    <Select.Label>Select colour scheme</Select.Label>
  </div>
  <Select.Trigger placeholder="Select theme..."></Select.Trigger>
  <Select.Options>
    {#each availableThemes as theme (theme)}
      <Select.Item value={theme} label={capitalise(theme)}></Select.Item>
    {/each}
  </Select.Options>
</Select.Root>
