"use client";

import GameChat from "@/components/GameChat";

interface ChatMessage {
  id: string;
  sender: string;
  text: string;
}

export async function sendChatHistoryToLLM(messages: ChatMessage[]): Promise<boolean> {
  try {
    const res = await fetch("http://127.0.0.1:5000/summarise_chat_history", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "sentences": messages }),
    });
    if (!res.ok) return false;
    return true;
  } catch {
    return false;
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