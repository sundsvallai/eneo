<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Settings } from "$lib/components/layout";
  import type { TokenUsageSummary } from "@intric/intric-js";
  import TokenOverviewBar from "./TokenOverviewBar.svelte";
  import TokenOverviewTable from "./TokenOverviewTable.svelte";
  import { CalendarDate } from "@internationalized/date";
  import { getIntric } from "$lib/core/Intric";
  import { Input } from "@intric/ui";

  type Props = {
    tokenStats: TokenUsageSummary;
  };

  const { tokenStats }: Props = $props();
  let detailedStats = $state(tokenStats);

  const intric = getIntric();

  const now = new Date();
  const today = new CalendarDate(now.getFullYear(), now.getMonth() + 1, now.getUTCDate());
  let dateRange = $state({
    start: today.subtract({ days: 30 }),
    end: today
  });

  async function update(timeframe: { start: CalendarDate; end: CalendarDate }) {
    detailedStats = await intric.usage.tokens.getSummary({
      startDate: timeframe.start.toString(),
      // We add one day so the end day includes the whole day. otherwise this would be interpreted as 00:00
      endDate: timeframe.end.add({ days: 1 }).toString()
    });
  }

  $effect(() => {
    if (dateRange.start && dateRange.end) {
      update(dateRange);
    }
  });
</script>

<Settings.Page>
  <Settings.Group title="Overview">
    <TokenOverviewBar {tokenStats}></TokenOverviewBar>
  </Settings.Group>
  <Settings.Group title="Details">
    <Settings.Row
      title="Usage by model"
      description="See this organisation's token usage by models and timeframe."
      fullWidth
    >
      <div slot="toolbar">
        <Input.DateRange bind:value={dateRange}></Input.DateRange>
      </div>
      <TokenOverviewTable tokenStats={detailedStats}></TokenOverviewTable>
    </Settings.Row>
  </Settings.Group>
</Settings.Page>
