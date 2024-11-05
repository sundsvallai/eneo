<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { initSpacesManager } from "$lib/features/spaces/SpacesManager.js";

  export let data;

  initSpacesManager(data);
</script>

<slot />
