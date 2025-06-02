const unsupportedModels = ["o3-mini-azure", "o3-mini"];

export function supportsTemperature(modelName?: string): boolean {
  return modelName ? !unsupportedModels.includes(modelName) : false;
}
