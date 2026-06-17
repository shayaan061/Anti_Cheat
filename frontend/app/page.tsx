import WebcamFaceTracker from "@/components/WebcamFaceTracker";

export default function Home() {
  return (
    <main className="relative w-screen h-screen overflow-hidden">

      {/* Background Screenshot */}
      <img
        src="/interview-ui.png"
        alt="Interview UI"
        className="absolute inset-0 w-full h-full object-cover"
      />

      {/* Camera Overlay */}
      <div
        className="
          absolute
          overflow-hidden
          rounded-2xl
        "
        style={{
          left: "53%",
          top: "10%",
          width: "25%",
          height: "70%",
        }}
      >
        <WebcamFaceTracker />
      </div>
    </main>
  );
}