<script lang="ts">
  import { IconMicrophone } from "@intric/icons/microphone";
  import { IconStop } from "@intric/icons/stop";
  import { Tooltip } from "@intric/ui";
  import { onDestroy, onMount } from "svelte";

  import dayjs from "dayjs";

  export let onRecordingDone: (params: { blob: Blob; mimeType: string }) => void;

  let isRecording: boolean = false;
  let startedRecordingAt = dayjs();
  let elapsedTime = "";
  let volumeMeter: HTMLMeterElement | undefined;

  let mediaStream: MediaStream | null;
  let mediaStreamNode: MediaStreamAudioSourceNode | null;
  let mediaRecorder: MediaRecorder | null;
  let audioContext: AudioContext | null;
  let analyserNode: AnalyserNode | null;
  let levelBuffer = new Float32Array();

  let recordingBuffer: Blob[] = [];
  let recordedBlob: Blob | null = null;
  let audioURL: string | null = null;

  function startRecording() {
    recordingBuffer = [];
    isRecording = true;
    startedRecordingAt = dayjs();

    if (mediaStream) {
      const mimeType = MediaRecorder.isTypeSupported("audio/mp4;codecs=avc1")
        ? "audio/mp4;codecs=avc1"
        : "audio/webm;codecs=opus";

      mediaRecorder = new MediaRecorder(mediaStream, {
        mimeType
      });

      mediaRecorder.addEventListener("dataavailable", (event) => {
        recordingBuffer.push(event.data);
      });

      mediaRecorder.addEventListener("stop", () => {
        recordedBlob = new Blob(recordingBuffer, { type: mimeType });
        audioURL = URL.createObjectURL(recordedBlob);
        onRecordingDone({ blob: recordedBlob, mimeType });
      });

      mediaRecorder.start();
    }
  }

  function stopRecording() {
    isRecording = false;
    mediaRecorder?.stop();
  }

  function toggleRecording(e: Event) {
    e.preventDefault();
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  }

  const onAnimationFrame = () => {
    if (volumeMeter) {
      analyserNode?.getFloatTimeDomainData(levelBuffer);
      let sumSquares = 0.0;
      for (const amplitude of levelBuffer) {
        sumSquares += amplitude * amplitude;
      }
      volumeMeter.value = Math.sqrt(sumSquares / levelBuffer.length);
    }
    elapsedTime = formatElapsed(dayjs().diff(startedRecordingAt, "seconds"));
    window.requestAnimationFrame(onAnimationFrame);
  };

  const formatElapsed = (seconds: number) => {
    const mm = Math.floor(seconds / 60)
      .toString()
      .padStart(2, "0");
    const ss = (seconds % 60).toString().padStart(2, "0");
    return `${mm}:${ss}`;
  };

  onMount(async () => {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        noiseSuppression: true,
        echoCancellation: true,
        autoGainControl: true
      }
    });

    audioContext = new AudioContext();
    analyserNode = audioContext.createAnalyser();
    levelBuffer = new Float32Array(analyserNode.fftSize);
    mediaStreamNode = audioContext.createMediaStreamSource(mediaStream);
    mediaStreamNode.connect(analyserNode);
    window.requestAnimationFrame(onAnimationFrame);
  });

  onDestroy(() => {
    mediaStream?.getAudioTracks().forEach((track) => {
      track.stop();
    });
    mediaStream = null;
  });
</script>

<div class="flex flex-col items-center justify-center gap-2">
  <div data-is-recording={isRecording} class="recording-widget">
    <Tooltip text={isRecording ? "Stop recording" : "Start recording"}>
      <button class="record-button" on:click={toggleRecording} data-is-recording={isRecording}>
        {#if !isRecording}
          <IconMicrophone />
        {:else}
          <IconStop />
        {/if}
      </button>
    </Tooltip>

    {#if isRecording}
      <div class="px-6 py-2 font-mono">Time: {elapsedTime}</div>
    {:else if audioURL}
      <audio controls src={audioURL} class="ml-2 h-12 rounded-full border border-stronger shadow-sm"
      ></audio>
    {:else}
      <div class="flex flex-col items-center justify-center px-6">
        <meter bind:this={volumeMeter} min="0" high="0.7" optimum="0.5" max="0.8" value="0"></meter>
      </div>
    {/if}
  </div>
</div>

<style lang="postcss">
  .record-button {
    @apply flex h-12 w-12 items-center justify-center rounded-full bg-negative-default text-on-fill hover:bg-negative-stronger;
  }

  .record-button[data-is-recording="true"] {
    @apply bg-primary text-negative-stronger hover:bg-negative-dimmer hover:text-negative-stronger;
  }

  .recording-widget {
    @apply flex items-center rounded-full border border-stronger bg-primary p-2 shadow-lg;
  }

  .recording-widget[data-is-recording="true"] {
    @apply bg-negative-default text-on-fill;
  }

  /* meter {
    -webkit-appearance: none;
  } */

  meter::-webkit-meter-inner-element {
    @apply !h-4 overflow-clip rounded-full;
  }

  meter::-webkit-meter-bar {
    @apply !h-4 overflow-clip rounded-full;
  }
</style>
