"use client";

import GameChat from "@/components/GameChat";

export default function Page() {
  return (
    <main style={{ display: "grid", placeItems: "center", minHeight: "100vh" }}>
      <GameChat
        playerName="Player1"
        onEnd={(session) => console.log("Chat ended:", session)}
      />
    </main>
  );
}