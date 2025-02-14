<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script context="module" lang="ts">
  import type { CompletionModel, EmbeddingModel } from "@intric/intric-js";
  import { Label } from "@intric/ui";
  export function getLabels(model: CompletionModel | EmbeddingModel) {
    const labels: {
      label: string | number;
      color: Label.LabelColor;
      tooltip: string;
    }[] = [];

    if ("vision" in model && model.vision) {
      labels.push({
        tooltip: "This model can process image files",
        label: "Vision",
        color: "gold"
      });
    }

    if (model.open_source) {
      labels.push({
        tooltip: "This model is open source",
        label: "Open Source",
        color: "green"
      });
    }

    if (model.hosting !== null) {
      labels.push({
        tooltip: "Region this model is hosted in",
        label: model.hosting.toUpperCase(),
        color: model.hosting === "usa" ? "orange" : "green"
      });
    }

    // if (model.stability === "experimental") {
    //   labels.push({
    //     tooltip: "Stability",
    //     label: "Experimental",
    //     color: "yellow"
    //   });
    // }

    return labels;
  }
</script>

<script lang="ts">
  export let model: CompletionModel | EmbeddingModel;
  $: labels = getLabels(model);
</script>

<Label.List content={labels} />
