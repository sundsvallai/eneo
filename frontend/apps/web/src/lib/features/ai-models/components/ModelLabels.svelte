<!-- MIT License -->
<script context="module" lang="ts">
  import type { CompletionModel, EmbeddingModel } from "@intric/intric-js";
  import { Label } from "@intric/ui";
  export function getLabels(model: CompletionModel | EmbeddingModel) {
    const labels: {
      label: string | number;
      color: Label.LabelColor;
      tooltip: string;
    }[] = [];

    if ("token_limit" in model && model.token_limit !== null) {
      labels.push({
        tooltip: "Context length in tokens",
        label: `Context: ${Math.floor(model.token_limit / 1000)}K`,
        color: "blue"
      });
    }

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
        tooltip: "Hosting",
        label: model.hosting.toUpperCase(),
        color: model.hosting === "usa" ? "orange" : "green"
      });
    }

    if (model.stability === "experimental") {
      labels.push({
        tooltip: "Stability",
        label: "Experimental",
        color: "yellow"
      });
    }

    return labels;
  }
</script>

<script lang="ts">
  export let model: CompletionModel | EmbeddingModel;
  const labels = getLabels(model);
</script>

<Label.List content={labels} />
