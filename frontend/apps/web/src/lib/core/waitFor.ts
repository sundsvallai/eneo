/**
 * Run a side-effect after awaiting a value
 *
 * Use case: When loading an assistant, we want it to be possible to send in the history as a promise,
 * so we can immediately show the chat view without awaiting the whole history. This requires the history
 * to be initialised as an empty array, and, once the promise is resolved, the array has to be updated.
 * However, there could also be no history at all in which case we would (maybe) want to set a fallback
 * value. The idea is to have this function behave as if we could subscribe to the inital value.
 *
 * @param  data A promise you want to await (or just straight up the data, this takes both)
 * @param {Object} fns
 * @param fns.onLoaded A callback to run with the awaited promise
 * @param fns.onNull An optional callback to run when the promise resolves to null or no data is present
 * */
export async function waitFor<T>(
  data: T | Promise<T> | null,
  fns: {
    onLoaded: (loadedData: NonNullable<T>) => void;
    onNull?: () => void;
  }
) {
  if (!data) {
    fns.onNull?.();
    return;
  }

  const loaded = data instanceof Promise ? await data : data;

  if (loaded) {
    fns.onLoaded(loaded);
  } else {
    fns.onNull?.();
  }
}
