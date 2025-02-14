type AssistantTemplateCategory = "communication" | "q&a" | "misc" | "advice";

export const assistantTemplateCategories: Record<
  AssistantTemplateCategory,
  { title: string; description: string }
> = {
  communication: {
    title: "Kommunikation",
    description: "Assistenter som förbättrar tydlighet och kvalitet i din kommunikation."
  },
  "q&a": {
    title: "Frågor & Svar",
    description: "Assistenter som ger informativa och klara svar på vanliga frågor."
  },

  advice: {
    title: "Rådgivning",
    description: "Assistenter som vägleder genom beslutsfattande och kreativa processer."
  },
  misc: {
    title: "Övrigt",
    description: "Diverse assistenter för olika behov och uppgifter."
  }
} as const;

type AppTemplateCategory = "transcription" | "misc";

export const appTemplateCategories: Record<
  AppTemplateCategory,
  { title: string; description: string }
> = {
  transcription: {
    title: "Transkription",
    description: "Appar som hjälper till med att transkribera och dokumentera tal och möten."
  },
  misc: {
    title: "Övrigt",
    description: "Diverse appar för olika funktioner och behov."
  }
} as const;
