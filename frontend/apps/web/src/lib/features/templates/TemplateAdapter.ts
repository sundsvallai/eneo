import type { AppTemplate, AssistantTemplate, Intric, JSONRequestBody } from "@intric/intric-js";
import { appTemplateCategories, assistantTemplateCategories } from "./TemplateCategories";

export type GenericTemplate = {
  [K in keyof AssistantTemplate & keyof AppTemplate]: AssistantTemplate[K] | AppTemplate[K];
};

// Creating an app from template has the same request body, so we can use the assistant one for both of them
type TemplateCreateRequest = JSONRequestBody<
  "post",
  "/api/v1/spaces/{id}/applications/assistants/"
>;

export type TemplateAdapter = {
  type: "assistants" | "apps";
  getTemplates: () => Promise<GenericTemplate[]>;
  createNew: (params: TemplateCreateRequest) => Promise<{ id: string }>;
  getResourceName: () => { singular: string; singularCapitalised: string };
  getCategorisedTemplates: (templates: GenericTemplate[]) => {
    title: string;
    description: string;
    templates: GenericTemplate[];
  }[];
};

export function createAssistantTemplateAdapter(params: {
  intric: Intric;
  currentSpaceId: string;
}): TemplateAdapter {
  const { intric, currentSpaceId } = params;

  return {
    type: "assistants",
    async getTemplates() {
      return await intric.templates.list({ filter: "assistants" });
    },
    async createNew({ from_template, name }: TemplateCreateRequest) {
      return await intric.assistants.create({ spaceId: currentSpaceId, name, from_template });
    },
    getResourceName() {
      return { singular: "assistant", singularCapitalised: "Assistant" };
    },
    getCategorisedTemplates(templates) {
      return Object.entries(assistantTemplateCategories).map(([category, info]) => {
        return {
          ...info,
          templates: templates.filter((template) => template.category === category)
        };
      });
    }
  };
}

export function createAppTemplateAdapter(params: {
  intric: Intric;
  currentSpaceId: string;
}): TemplateAdapter {
  const { intric, currentSpaceId } = params;

  return {
    type: "apps",
    async getTemplates() {
      return await intric.templates.list({ filter: "apps" });
    },
    async createNew({ from_template, name }: TemplateCreateRequest) {
      return await intric.apps.create({ spaceId: currentSpaceId, name, from_template });
    },
    getResourceName() {
      return { singular: "app", singularCapitalised: "App" };
    },
    getCategorisedTemplates(templates) {
      return Object.entries(appTemplateCategories).map(([category, info]) => {
        return {
          ...info,
          templates: templates.filter((template) => template.category === category)
        };
      });
    }
  };
}
