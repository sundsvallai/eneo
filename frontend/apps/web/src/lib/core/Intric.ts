import type { Intric } from "@intric/intric-js";
import { createContext } from "./context";

const [getIntric, setIntric] = createContext<Intric>("Authenticated intric client");

function initIntric(data: { intric: Intric }) {
  setIntric(data.intric);
}

export { initIntric, getIntric };
