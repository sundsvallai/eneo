/**
 *  This is a Work-in-progress concept for adding websockets
 */

import type { IntricSocket } from "@intric/intric-js";
import { createContext } from "./context";

const [getIntricSocket, setIntricSocket] = createContext<IntricSocket>(
  "Authenticated intric socket"
);

function initIntricSocket(data: { intricSocket: IntricSocket }) {
  setIntricSocket(data.intricSocket);
  return data.intricSocket;
}

export { initIntricSocket, getIntricSocket };
