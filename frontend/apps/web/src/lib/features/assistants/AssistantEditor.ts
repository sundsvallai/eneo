import { createContext } from "$lib/core/context";
import { createResourceEditor } from "$lib/core/editing/ResourceEditor";
import type { Intric, Assistant } from "@intric/intric-js";

const [getAssistantEditor, setAssistantEditor] =
  createContext<ReturnType<typeof initAssistantEditor>>("Edit an Assistant");

/**
 * Initialise the ResourceEditor in its context.
 * Retrieve it via `getAssistantEditor()`
 */
function initAssistantEditor(data: {
  assistant: Assistant;
  intric: Intric;
  onUpdateDone?: (assistant: Assistant) => void;
}) {
  const editor = createResourceEditor({
    intric: data.intric,
    resource: data.assistant,
    defaults: {
      prompt: { description: "", text: "" }
    },
    updateResource: async (resource, changes) => {
      const updated = await data.intric.assistants.update({ assistant: resource, update: changes });
      data.onUpdateDone?.(updated);
      return updated;
    },
    editableFields: {
      name: true,
      completion_model: ["id"],
      completion_model_kwargs: true,
      prompt: ["description", "text"],
      websites: ["id"],
      groups: ["id"],
      attachments: ["id"]
    },
    manageAttachements: "attachments"
  });
  setAssistantEditor(editor);
  return editor;
}
export { initAssistantEditor, getAssistantEditor };
