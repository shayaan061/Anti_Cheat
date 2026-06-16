"use client";

import { useEffect, useRef } from "react";

import {
  FaceLandmarker,
  FilesetResolver,
} from "@mediapipe/tasks-vision";

export default function WebcamFaceTracker() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let faceLandmarker: FaceLandmarker;

    async function initialize() {
      const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
      );

      faceLandmarker = await FaceLandmarker.createFromOptions(
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

      // Connect WebSocket

      socketRef.current = new WebSocket(
        "ws://localhost:8000/ws/pose"
      );

      socketRef.current.onopen = () => {
        console.log("WebSocket Connected");

        socketRef.current?.send(
          JSON.stringify({
            sessionId: "test123",
          })
        );
      };

      socketRef.current.onmessage = (event) => {
        console.log(
          "Backend Response:",
          JSON.parse(event.data)
        );
      };

      socketRef.current.onerror = (error) => {
        console.error(
          "WebSocket Error:",
          error
        );
      };

      requestAnimationFrame(detectLoop);
    }

    async function detectLoop() {
      if (!videoRef.current) {
        requestAnimationFrame(detectLoop);
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
        const face = result.faceLandmarks[0];

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
  socketRef.current.readyState === WebSocket.OPEN
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

      requestAnimationFrame(detectLoop);
    }

    initialize();

    return () => {
      faceLandmarker?.close();

      socketRef.current?.close();
    };
  }, []);

  return (
    <video
      ref={videoRef}
      autoPlay
      muted
      playsInline
      style={{
        width: "800px",
        border: "1px solid black",
      }}
    />
  );
}