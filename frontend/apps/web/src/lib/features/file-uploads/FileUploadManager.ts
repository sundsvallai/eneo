// MIT License

import { derived, get, writable } from "svelte/store";
import type { Intric, UploadedFile } from "@intric/intric-js";
import { createContext } from "$lib/core/context";

type Upload = {
  id: string;
  file: File;
  status: "queued" | "uploading" | "completed";
  progress: number;
  fileRef?: UploadedFile;
};

export const [getFileUploadManager, setFileUploadManager] =
  createContext<ReturnType<typeof createFileUploadManager>>();

export function createFileUploadManager(intric: Intric) {
  const currentUploads = writable<Upload[]>([]);
  const waitingUploads = derived(currentUploads, (uploads) =>
    uploads.filter((upload) => upload.status === "queued")
  );
  const runningUploads = derived(currentUploads, (uploads) =>
    uploads.filter((upload) => upload.status === "uploading")
  );
  const isBusy = derived(
    currentUploads,
    (uploads) => uploads.filter((upload) => upload.status !== "completed").length > 0
  );

  const max_upload_connections = 5;

  function queueUploads(files: File[]) {
    files.forEach((file) => {
      const id = crypto.randomUUID();
      const upload: Upload = { id, file, status: "queued", progress: 0 }; // Ensure correct type here
      currentUploads.update((uploads) => [...uploads, upload]);
    });

    continueUploadQueue();
  }

  function continueUploadQueue() {
    while (
      get(runningUploads)?.length < max_upload_connections &&
      get(waitingUploads)?.length > 0
    ) {
      const upload = get(waitingUploads)[0];
      if (upload) {
        currentUploads.update((uploads) =>
          uploads.map((u) => {
            if (u.id === upload.id) {
              u.status = "uploading";
            }
            return u;
          })
        );
        intric.files
          .upload({
            file: upload.file,
            onProgress: (ev) => {
              currentUploads.update((uploads) =>
                uploads.map((u) => {
                  if (u.id === upload.id) {
                    u.progress = Math.floor((ev.loaded / ev.total) * 100);
                  }
                  return u;
                })
              );
            }
          })
          .then((fileRef) => {
            currentUploads.update((uploads) =>
              uploads.map((u) => {
                if (u.id === upload.id) {
                  u.fileRef = fileRef;
                  u.status = "completed";
                }
                return u;
              })
            );
            continueUploadQueue();
          })
          .catch((error) => {
            alert(
              `We encountered an error uploading the file ${upload.file.name}\n${error.message}`
            );
            currentUploads.update((uploads) => uploads.filter((u) => u.id !== upload.id));
            console.error("Upload error:", error);
            continueUploadQueue();
          });
      }
    }
  }

  async function removeUpload(fileRef: UploadedFile) {
    // This can fail, but that's ok
    try {
      await intric.files.delete({ fileId: fileRef.id });
    } finally {
      // We always remove from our list, so it is not included in the question
      currentUploads.update((uploads) =>
        uploads.filter((upload) => upload.fileRef?.id !== fileRef.id)
      );
    }
  }

  function clearUploads() {
    currentUploads.set([]);
  }

  return {
    state: {
      uploads: { subscribe: currentUploads.subscribe },
      isBusy: { subscribe: isBusy.subscribe }
    },
    queueUploads,
    clearUploads,
    removeUpload
  };
}
