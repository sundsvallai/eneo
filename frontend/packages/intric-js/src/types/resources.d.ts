import { components } from "./schema";

export type Assistant = components["schemas"]["AssistantPublicWithUser"];
export type AssistantSparse = components["schemas"]["AssistantSparse"];
export type AssistantResponse = Omit<components["schemas"]["AskResponse"], "session_id"> & {
  session_id?: string | undefined;
  id?: string | undefined;
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
export type CompletionModel = components["schemas"]["CompletionModelPublic"];
export type EmbeddingModel = components["schemas"]["EmbeddingModelPublic"];
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
