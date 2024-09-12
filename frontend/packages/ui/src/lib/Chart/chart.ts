import { registerTheme, init, type EChartsCoreOption } from "echarts";
import type { Action } from "svelte/action";
import { intricTheme } from "./theme.js";

export type Config = {
  options: EChartsCoreOption;
  theme?: string | object;
  renderer?: "canvas" | "svg";
};

registerTheme("intric", intricTheme);

export const chart: Action<HTMLElement, Config> = (node, params) => {
  const { theme = "intric", renderer = "canvas" } = params;
  const options: EChartsCoreOption = {
    aria: {
      enabled: true
    },
    tooltip: {
      show: true
    },
    grid: {
      left: 0,
      top: 5,
      right: 5,
      bottom: 0,
      containLabel: true
    },
    ...params.options
  };

  const chart = init(node, theme, { renderer });
  chart.setOption(options);

  const resizeObserver = new ResizeObserver(() => chart.resize());
  resizeObserver.observe(node);

  return {
    destroy() {
      chart.dispose();
      resizeObserver.disconnect();
    },

    update(newParams: Config) {
      chart.setOption({
        ...params.options,
        ...newParams.options
      });
    }
  };
};
