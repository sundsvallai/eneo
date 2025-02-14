import { components } from "./schema";

export type Assistant =
  | components["schemas"]["AssistantPublic"]
  | components["schemas"]["DefaultAssistant"];
export type AssistantSparse = components["schemas"]["AssistantSparse"];
export type AssistantResponse = Omit<
  components["schemas"]["AskResponse"],
  "session_id" | "references" | "tools"
> & {
  session_id?: string | undefined;
  id?: string | undefined;
  created_at?: string | null | undefined;
  tools?: components["schemas"]["UseTools"];
  references: Omit<components["schemas"]["InfoBlobAskAssistantPublic"], "score">[];
};
export type AssistantSession = components["schemas"]["SessionPublic"];
export type Service = components["schemas"]["ServicePublicWithUser"];
export type ServiceSparse = components["schemas"]["ServiceSparse"];
export type Group = Omit<
  components["schemas"]["GroupPublicWithMetadata"],
  "embedding_model" | "user"
> & {
  embedding_model?: components["schemas"]["EmbeddingModelSparse"] | null | undefined;
};
export type GroupSparse = components["schemas"]["GroupSparse"];
export type InfoBlob = Omit<components["schemas"]["InfoBlobPublic"], "text"> & {
  text?: string | undefined;
};
export type Widget = components["schemas"]["WidgetPublic"];
export type CompletionModel = components["schemas"]["CompletionModel"];
export type EmbeddingModel = components["schemas"]["EmbeddingModel"];
export type Job = components["schemas"]["JobPublic"];
export type JobStatus = components["schemas"]["JobStatus"];
export type Tenant = components["schemas"]["TenantPublic"];
export type UserGroup = components["schemas"]["UserGroupPublic"];
export type User = components["schemas"]["UserAdminView"];
export type UserSparse = components["schemas"]["UserSparse"];
export type CurrentUser = components["schemas"]["UserPublic"];
export type Role = components["schemas"]["RolePublic"];
export type Permission = components["schemas"]["Permission"];
export type ResourcePermission = components["schemas"]["ResourcePermission"];
export type CrawlRun = components["schemas"]["CrawlRunPublic"];
export type Limits = components["schemas"]["Limits"];
export type UploadedFile = components["schemas"]["FilePublic"];
export type Website = components["schemas"]["WebsitePublic"];
export type WebsiteSparse = components["schemas"]["WebsiteSparse"];
export type ModelCreatorOrg = components["schemas"]["Orgs"];
export type Space = components["schemas"]["SpacePublic"];
export type SpaceSparse = components["schemas"]["SpaceSparse"];
export type Dashboard = components["schemas"]["Dashboard"];
export type Prompt = components["schemas"]["PromptPublic"];
export type PromptSparse = components["schemas"]["PromptSparse"];
export type IntricErrorCode = components["schemas"]["ErrorCodes"] | 0;
export type App = components["schemas"]["AppPublic"];
export type AppSparse = components["schemas"]["AppSparse"];
export type AppRun = components["schemas"]["AppRunPublic"];
export type AppRunSparse = components["schemas"]["AppRunSparse"];
export type AppRunInput = components["schemas"]["AppRunInput"];
export type AssistantTemplate = components["schemas"]["AssistantTemplatePublic"];
export type AppTemplate = components["schemas"]["AppTemplatePublic"];
export type TemplateAdditionalField = components["schemas"]["AdditionalField"];
export type SpaceRole = components["schemas"]["SpaceRole"];
export type StorageSpaceInfo = components["schemas"]["StorageSpaceInfoModel"];

export type Paginated<T> = {
  items: T[];
  total_count: number;
  limit?: number | null;
  next_cursor?: string | null;
  previous_cursor?: string | null;
  count: number;
};

export type AnalyticsData = {
  assistants: {
    id: string;
    created_at: string;
  }[];
  sessions: {
    id: string;
    created_at: string;
    assistant_id: string;
  }[];
  questions: {
    id: string;
    created_at: string;
    assistant_id: string;
    session_id: string;
  }[];
};
