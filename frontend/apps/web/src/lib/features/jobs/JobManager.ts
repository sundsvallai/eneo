import { browser } from "$app/environment";
import { invalidate } from "$app/navigation";
import { createContext } from "$lib/core/context";
import { getIntric } from "$lib/core/Intric";
import type { Job } from "@intric/intric-js";
import { derived, writable } from "svelte/store";

export { getJobManager, initJobManager };

const [getJobManager, setJobManager] =
  createContext<ReturnType<typeof createJobManager>>("Handles jobs");

function initJobManager() {
  setJobManager(createJobManager());
}

function createJobManager() {
  const intric = getIntric();

  // Panel -------------------------------------------------------------------  //
  const showJobManagerPanel = writable(false);

  // Backend jobs -------------------------------------------------------------------  //
  let currentJobs: Map<string, Job> = new Map();
  const currentJobStore = writable<Job[]>([]);

  function addJob(job: Job) {
    currentJobs.set(job.id, job);
    currentJobStore.set([...currentJobs.values()]);
    startUpdatePolling();
  }

  // Keep track of how many times getting jobs has failed
  let jobUpdateErrors = 0;
  /** Will get all currently running jobs from the server */
  async function updateJobs(): Promise<Job[]> {
    let jobs: Job[] = [];
    try {
      jobs = await intric.jobs.list();
      // Reset errors on success
      jobUpdateErrors = 0;
    } catch (error) {
      console.error("JobManager: Could not get jobs from server", error);
      jobUpdateErrors += 1;
      // Returning an empyt array will cancel the job update Interval/update polling
      // This timeout starts if after 20 seconds if we do not have 5 consecutive errors
      if (jobUpdateErrors < 5) {
        setTimeout(() => {
          startUpdatePolling();
        }, 20 * 1000);
      }
      return [];
    }
    const updatedJobs = new Map(
      // For now we ignore failed jobs in the UI
      jobs
        .filter((job) => job.status === "in progress" || job.status === "queued")
        .map((job) => [job.id, job])
    );
    if (updatedJobs.size < currentJobs.size) {
      if (browser) {
        invalidate("blobs:list");
      }
    }
    currentJobs = updatedJobs;
    currentJobStore.set([...currentJobs.values()]);
    return jobs;
  }

  const updateJobsFrequency_ms = 30 * 1000;
  let updateJobsInterval: ReturnType<typeof setInterval>;
  let updateJobsRunning = false;
  async function startUpdatePolling() {
    if (updateJobsRunning === false) {
      updateJobsRunning = true;
      await updateJobs();
      updateJobsInterval = setInterval(async () => {
        const jobs = await updateJobs();
        if (jobs.length === 0) {
          stopUpdatePolling();
        }
      }, updateJobsFrequency_ms);
    }
  }

  // Entry point
  if (browser) {
    startUpdatePolling();
  }

  function stopUpdatePolling() {
    updateJobsRunning = false;
    clearInterval(updateJobsInterval);
  }

  // Uploading -------------------------------------------------------------------  //
  type Upload = {
    id: string;
    file: File;
    status: "queued" | "uploading" | "completed";
    /// Destination for this file
    groupId: string;
    progress: number;
  };

  const currentUploads: Map<string, Upload> = new Map();
  const currentUploadsStore = writable<Upload[]>([]);

  const waitingUploads: Set<string> = new Set();
  const runningUploads: Set<string> = new Set();
  const max_upload_connections = 5;

  function queueUploads(groupId: string, files: File[]) {
    files.forEach((file) => {
      const id = crypto.randomUUID();
      currentUploads.set(id, { id, file, status: "queued", progress: 0, groupId });
      waitingUploads.add(id);
    });

    continueUploadQueue();
  }

  function continueUploadQueue() {
    startSyncingUploads();
    while (runningUploads.size < max_upload_connections && waitingUploads.size > 0) {
      const uploadId = waitingUploads.values().next().value;
      waitingUploads.delete(uploadId);
      const upload = currentUploads.get(uploadId);
      if (upload) {
        runningUploads.add(uploadId);
        upload.status = "uploading";
        intric.infoBlobs
          .upload({
            group_id: upload.groupId,
            file: upload.file,
            onProgress: (ev) => {
              upload.progress = Math.floor((ev.loaded / ev.total) * 100);
            }
          })
          .then((job) => {
            // Delete from running uploads
            runningUploads.delete(uploadId);
            upload.status = "completed";
            addJob(job);
            // Delete from upload list
            // This does not directly update the store, but next time the store is updated this upload will no longer be included
            currentUploads.delete(upload.id);
            continueUploadQueue();
          })
          .catch((error) => {
            alert(
              `We encountered an error uploading the file ${upload.file.name}\n${error.message}`
            );
            runningUploads.delete(uploadId);
            currentUploads.delete(upload.id);
            console.error("Upload error:", error);
            continueUploadQueue();
          });
      }
    }
    currentUploadsStore.set([...currentUploads.values()]);
  }

  const uploadSyncFrequency_ms = 1000;
  let syncUploadsInterval: ReturnType<typeof setInterval>;
  let syncUploadsRunning = false;
  function startSyncingUploads() {
    if (syncUploadsRunning === false) {
      syncUploadsRunning = true;
      currentUploadsStore.set([...currentUploads.values()]);
      syncUploadsInterval = setInterval(async () => {
        currentUploadsStore.set([...currentUploads.values()]);
        if (runningUploads.size === 0 && waitingUploads.size === 0) {
          stopSyncingUploads();
        }
      }, uploadSyncFrequency_ms);
    }
  }

  function stopSyncingUploads() {
    syncUploadsRunning = false;
    clearInterval(syncUploadsInterval);
  }

  function clearFinishedUploads() {
    const remainingJobs = [...currentUploads.values()].filter(
      (upload) => upload.status !== "completed"
    );
    currentUploadsStore.set(remainingJobs);
  }

  const currentlyRunningJobs = derived(
    [currentJobStore, currentUploadsStore],
    ([jobs, uploads]) => {
      return jobs.length + uploads.length;
    }
  );

  return {
    state: {
      jobs: { subscribe: currentJobStore.subscribe },
      uploads: { subscribe: currentUploadsStore.subscribe },
      currentlyRunningJobs,
      showJobManagerPanel
    },
    queueUploads,
    clearFinishedUploads,
    updateJobs
  };
}
