<script lang="ts">
  import { createDateRangePicker } from "@melt-ui/svelte";
  import { CalendarDate, type DateValue } from "@internationalized/date";
  import Button from "$lib/Button/Button.svelte";
  import { Tooltip } from "$lib/Tooltip/index.js";
  import { IconCalendar } from "@intric/icons/calendar";

  const now = new Date();
  const today = new CalendarDate(now.getFullYear(), now.getMonth() + 1, now.getUTCDate());

  let cls = "";
  export { cls as class };

  export let value: {
    start: DateValue | undefined;
    end: DateValue | undefined;
  } = getDefaultRange();

  function getDefaultRange() {
    return {
      start: today.subtract({ weeks: 1 }),
      end: today
    };
  }

  const {
    elements: {
      overlay,
      arrow,
      calendar,
      cell,
      content,
      field,
      grid,
      heading,
      label,
      nextButton,
      prevButton,
      startSegment,
      endSegment,
      trigger
    },
    states: { months, headingValue, weekdays, segmentContents, open },
    helpers: { isDateDisabled, isDateUnavailable }
  } = createDateRangePicker({
    defaultValue: value,
    weekdayFormat: "short",
    locale: "en-GB",
    onValueChange: ({ next }) => {
      value = next;
      return next;
    },
    preventScroll: true,
    arrowSize: 12,
    minValue: new CalendarDate(2023, 1, 1),
    maxValue: today
  });

  // When doing "use:field" svelte-check complains about the number of arguments... this "fixes" it for now
  const fieldWrap = (_: unknown) => field(); // eslint-disable-line @typescript-eslint/no-unused-vars
</script>

<div class="flex items-center justify-between gap-4 {cls}">
  <span {...$label} use:label class=""
    >{#if $$slots.default}<slot />{:else}Select timeframe{/if}</span
  >
  <div {...$field} use:fieldWrap class="mt-0 flex items-center gap-1">
    <div
      class="flex h-10 min-w-[220px] items-center justify-between gap-0.5 overflow-hidden rounded-lg border
  border-default bg-primary px-3 py-2 text-center shadow ring-default placeholder:text-muted focus-within:ring-2 hover:ring-2 focus-visible:ring-2"
    >
      {#each $segmentContents.start as seg}
        <div {...$startSegment(seg.part)} use:startSegment>
          {seg.value}
        </div>
      {/each}
      <div aria-hidden="true" class="px-1">–</div>
      {#each $segmentContents.end as seg}
        <div {...$endSegment(seg.part)} use:endSegment>
          {seg.value}
        </div>
      {/each}
    </div>
    <Tooltip text="Open calendar" asFragment let:trigger={tooltipTrigger} placement="top">
      <Button is={[$trigger, ...tooltipTrigger]} variant="primary" padding="icon">
        <IconCalendar />
      </Button>
    </Tooltip>
  </div>
</div>

{#if open}
  <div {...$overlay} use:overlay class="fixed inset-0 z-[90]" />
  <div
    {...$content}
    use:content
    class="relative z-[100] rounded-md border border-stronger bg-primary shadow-md"
  >
    <div {...$calendar} use:calendar class="relative z-10 rounded-md bg-primary p-2">
      <header class="flex items-center justify-between pb-2">
        <Button is={[$prevButton]} variant="outlined" class="!px-3">←</Button>
        <div {...$heading} use:heading class="font-mono">
          {$headingValue}
        </div>
        <Button is={[$nextButton]} variant="outlined" class="!px-3">→</Button>
      </header>
      <div>
        {#each $months as month}
          <table {...$grid} use:grid>
            <thead aria-hidden="true">
              <tr>
                {#each $weekdays as day}
                  <th>
                    <div>
                      {day}
                    </div>
                  </th>
                {/each}
              </tr>
            </thead>
            <tbody>
              {#each month.weeks as weekDates}
                <tr>
                  {#each weekDates as date}
                    <td
                      role="gridcell"
                      aria-disabled={$isDateDisabled(date) || $isDateUnavailable(date)}
                    >
                      <div {...$cell(date, month.value)} use:cell>
                        {date.day}
                      </div>
                    </td>
                  {/each}
                </tr>
              {/each}
            </tbody>
          </table>
        {/each}
      </div>
    </div>
    <div {...$arrow} use:arrow class="!z-0 border border-stronger" />
  </div>
{/if}

<style lang="postcss">
  [data-melt-datefield-field][data-invalid] {
    @apply border-negative-stronger;
  }

  [data-melt-datefield-segment] {
    @apply font-mono;
  }

  [data-melt-datefield-segment][data-invalid] {
    @apply text-negative-default;
  }

  [data-melt-calendar-grid] {
    @apply w-full;
  }

  [data-melt-calendar-cell] {
    @apply relative z-0 flex h-10 w-10 cursor-pointer select-none items-center justify-center rounded p-4 hover:bg-hover-default focus:z-10 focus:ring-4 focus:ring-[var(--text-primary)];
  }

  [data-melt-calendar-cell][data-highlighted] {
    @apply bg-accent-dimmer;
  }

  [data-melt-calendar-cell][data-range-highlighted] {
    @apply bg-accent-dimmer;
  }

  [data-melt-calendar-cell][data-disabled] {
    @apply pointer-events-none opacity-40;
  }

  [data-melt-calendar-cell][data-unavailable] {
    @apply pointer-events-none text-negative-default line-through;
  }

  [data-melt-calendar-cell][data-selected] {
    @apply bg-accent-default text-on-fill;
  }

  [data-melt-calendar-cell][data-outside-visible-months] {
    @apply pointer-events-none cursor-default opacity-40 hover:bg-transparent;
  }

  [data-melt-calendar-cell][data-outside-month] {
    @apply pointer-events-none cursor-default opacity-0 hover:bg-transparent;
  }
</style>
