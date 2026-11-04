"use client";

import GameChat from "@/components/GameChat";

interface ChatMessage {
  id: string;
  sender: string;
  text: string;
  pending: boolean; // true while waiting for the rephrased version
}

export async function sendChatHistoryToLLM(messages: ChatMessage[]): Promise<string> {
  try {
    const msg = messages
      .filter((m) => !m.pending)
      .map((m) => m.text.trim())
      .filter((t) => t.length > 0);
    
    const res = await fetch("http://127.0.0.1:5000/gives_verdict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "sentences": msg }),
    });
    if (!res.ok) return "";

    const data = await res.json()
    console.log("Data Received [verdict]: ", data.message)
    return data.message;
  } catch {
    return "";
  }
}

export default function Page() {
  return (
    <main style={{ display: "grid", placeItems: "center", minHeight: "100vh" }}>
      <GameChat
        playerName="Player1"
        onEnd={(messages) => sendChatHistoryToLLM(messages)}
      />
    </main>
  );
}