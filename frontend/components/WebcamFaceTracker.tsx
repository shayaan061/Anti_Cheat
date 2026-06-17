"use client";

import { useEffect, useRef, useState } from "react";

import {
  FaceLandmarker,
  FilesetResolver,
} from "@mediapipe/tasks-vision";

export default function WebcamFaceTracker() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const socketRef = useRef<WebSocket | null>(null);

  const [poseInfo, setPoseInfo] = useState({
    pitch: 0,
    yaw: 0,
    roll: 0,
    direction: "CENTER",
  });

  const [isCalibrated, setIsCalibrated] =
    useState(false);

  const [baselinePitch, setBaselinePitch] =
    useState(0);

  const [baselineYaw, setBaselineYaw] =
    useState(0);

  useEffect(() => {
    let faceLandmarker: FaceLandmarker;

    let lastFrameTime = 0;

    const FPS = 15;

    const FRAME_INTERVAL = 1000 / FPS;

    async function initialize() {
      const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
      );

      faceLandmarker =
        await FaceLandmarker.createFromOptions(
          vision,
          {
            baseOptions: {
              modelAssetPath:
                "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task",
            },
            runningMode: "VIDEO",
            numFaces: 1,
          }
        );

      const stream =
        await navigator.mediaDevices.getUserMedia({
          video: {
            width: 1280,
            height: 720,
          },
        });

      if (!videoRef.current) return;

      videoRef.current.srcObject = stream;

      await videoRef.current.play();

      socketRef.current = new WebSocket(
        "ws://localhost:8000/ws/pose"
      );

      socketRef.current.onopen = () => {
        console.log("WebSocket Connected");
      };

      socketRef.current.onmessage = (
        event
      ) => {
        const data = JSON.parse(
          event.data
        );

        if (data.type === "pose") {
          setPoseInfo({
            pitch: data.pitch,
            yaw: data.yaw,
            roll: data.roll,
            direction: data.direction,
          });

          setIsCalibrated(
            data.isCalibrated
          );

          setBaselinePitch(
            data.baselinePitch || 0
          );

          setBaselineYaw(
            data.baselineYaw || 0
          );
        }
      };

      socketRef.current.onerror = (
        error
      ) => {
        console.error(
          "WebSocket Error:",
          error
        );
      };

      requestAnimationFrame(
        detectLoop
      );
    }

    async function detectLoop() {
      const now = performance.now();

      if (
        now - lastFrameTime <
        FRAME_INTERVAL
      ) {
        requestAnimationFrame(
          detectLoop
        );
        return;
      }

      lastFrameTime = now;

      if (!videoRef.current) {
        requestAnimationFrame(
          detectLoop
        );
        return;
      }

      const result =
        faceLandmarker.detectForVideo(
          videoRef.current,
          performance.now()
        );

      if (
        result.faceLandmarks &&
        result.faceLandmarks.length > 0
      ) {
        const face =
          result.faceLandmarks[0];

        const width =
          videoRef.current.videoWidth;

        const height =
          videoRef.current.videoHeight;

        const poseData = {
          nose: {
            x: face[1].x * width,
            y: face[1].y * height,
          },

          chin: {
            x: face[152].x * width,
            y: face[152].y * height,
          },

          leftEye: {
            x: face[33].x * width,
            y: face[33].y * height,
          },

          rightEye: {
            x: face[263].x * width,
            y: face[263].y * height,
          },

          leftMouth: {
            x: face[61].x * width,
            y: face[61].y * height,
          },

          rightMouth: {
            x: face[291].x * width,
            y: face[291].y * height,
          },
        };

        if (
          socketRef.current &&
          socketRef.current.readyState ===
          WebSocket.OPEN
        ) {
          socketRef.current.send(
            JSON.stringify({
              sessionId: "test123",

              frameWidth: width,
              frameHeight: height,

              landmarks: poseData,
            })
          );
        }
      }

      requestAnimationFrame(
        detectLoop
      );
    }

    initialize();

    return () => {
      faceLandmarker?.close();
      socketRef.current?.close();
    };
  }, []);

  return (
    <div className="relative w-full h-full">

      <video
        ref={videoRef}
        autoPlay
        muted
        playsInline
        className="w-full h-full object-cover"
      />

      {!isCalibrated && (
        <div
          className="
            absolute
            inset-0
            bg-black/60
            flex
            items-center
            justify-center
          "
        >
          <div
            className="
              text-center
              text-white
            "
          >
            <div className="text-3xl font-bold">
              Calibrating...
            </div>

            <div className="mt-2">
              Please look naturally
              at the screen
            </div>
          </div>
        </div>
      )}

      {isCalibrated && (
        <div
          className="
            absolute
            top-4
            left-4
            bg-black/70
            text-white
            rounded-xl
            px-4
            py-3
            text-sm
          "
        >
          <div>
            Pitch: {poseInfo.pitch.toFixed(1)}
          </div>

          <div>
            Yaw: {poseInfo.yaw.toFixed(1)}
          </div>

          <div>
            Roll: {poseInfo.roll.toFixed(1)}
          </div>

          <div className="mt-2">
            Baseline Pitch:{" "}
            {baselinePitch.toFixed(1)}
          </div>

          <div>
            Baseline Yaw:{" "}
            {baselineYaw.toFixed(1)}
          </div>

          <div className="mt-2 font-bold">
            {poseInfo.direction}
          </div>

          <div className="text-green-400 mt-1">
            ✓ Calibrated
          </div>
        </div>
      )}

    </div>
  );
}