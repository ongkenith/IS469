"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import "./GameChat.css";

interface ChatMessage {
  id: string;
  sender: string;
  text: string;
  pending: boolean; // true while waiting for the rephrased version
}

type ChatStatus = "idle" | "active" | "ended";

interface GameChatProps {
  /** Name shown next to the user's messages. */
  playerName?: string;
  /** Called once when the user ends the chat, with the full history. */
  onEnd: (messages: ChatMessage[]) => void;
  /** Max characters per message. */
  maxLength?: number;
}

export async function predictMessage(message: ChatMessage): Promise<ChatMessage> {
  /* Call API to determine if message is offensive or not */
  try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "sentence": message }),
    });
    if (!res.ok) return message;

    const data = await res.json()
    console.log("Data Received [predict]: ", data)

    if (data.message === "[To be rewritten]") {
      return {"id": message.id, "sender": message.sender, "text": "[Your message is being rewritten...]", "pending": true}
    } else {
      return {"id": message.id, "sender": message.sender, "text": message.text, "pending": false}
    }
  } catch {
    return message;
  }
}

export async function sanitiseMessage(message: ChatMessage): Promise<ChatMessage> {
  /* Call API sanitise offensive message */
  try {
    const res = await fetch("http://127.0.0.1:5000/sanitise", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "sentence": message }),
    });
    if (!res.ok) return {"id": message.id, "sender": message.sender, "text": "*Message is offensive*", "pending": false};

    const data = await res.json()
    console.log("Data Received [sanitise]: ", data)
    
    return {"id": message.id, "sender": message.sender, "text": data.message, "pending": false}
  } catch {
    return {"id": message.id, "sender": message.sender, "text": "*Message is offensive*", "pending": false};
  }
}

function makeId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}


export default function GameChat({
  playerName = "You",
  onEnd
}: GameChatProps) {
  const [status, setStatus] = useState<ChatStatus>("idle");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [startedAt, setStartedAt] = useState<string | null>(null);
  const [endedAt, setEndedAt] = useState<string | null>(null);
  const [disableSubmit, setDisableSubmit] = useState<boolean>(false)

  const logRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Keep the newest line in view.
  useEffect(() => {
    const el = logRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages, status]);

  // Focus the input as soon as the chat opens.
  useEffect(() => {
    if (status === "active") inputRef.current?.focus();
  }, [status]);

  const startChat = () => {
    setMessages([]);
    setDraft("");
    setEndedAt(null);
    setStartedAt(new Date().toISOString());
    setStatus("active");
  };

  const endChat = () => {
    if (status !== "active" || !startedAt) return;
    onEnd(messages)
    setStatus("ended");
  };

  const sendMessage = async (e: FormEvent) => {
    e.preventDefault();
    setDisableSubmit(true)
    const text = draft.trim();
    if (!text || status !== "active") {
      setDisableSubmit(false)
      return;
    }

    setDraft("");

    const message = await predictMessage({
      id: makeId(),
      sender: playerName,
      text: text,
      pending: false,
    });

    setMessages((prev) => [...prev, message]);

    // Call Agent to get sanitised version
    if (message.pending === true) {
      const sanitised = await sanitiseMessage({"id": message.id, "sender": message.sender, "text": text, "pending": true});

      setMessages((prev) =>
        prev.map((m) =>
          m.id === message.id ? { ...sanitised } : m
        )
      );
    }

    setDisableSubmit(false)
    return
  };

  const isActive = status === "active";

  return (
    <>
      <section className="gc-root" aria-label="Game chat">

        <header className="gc-header">
          <div className="gc-title">
            <span
              className={`gc-dot ${isActive ? "gc-dot-on" : ""}`}
              aria-hidden="true"
            />
            <span>Chat</span>
            <span className="gc-status">
              {status === "idle" && "not started"}
              {status === "active" && "live"}
              {status === "ended" && "ended"}
            </span>
          </div>

          {isActive ? (
            <button type="button" className="gc-btn" onClick={endChat}>
              End chat
            </button>
          ) : (
            <button type="button" className="gc-btn" onClick={startChat}>
              {status === "ended" ? "Start new chat" : "Start chat"}
            </button>
          )}
        </header>

        <div
          className="gc-log"
          ref={logRef}
          role="log"
          aria-live="polite"
          aria-label="Chat messages"
        >
          {status === "idle" && (
            <p className="gc-empty">Press “Start chat” to begin.</p>
          )}

          {startedAt && (
            <p className="gc-system">Chat started at {formatTime(startedAt)}</p>
          )}

          {isActive && messages.length === 0 && (
            <p className="gc-empty">No messages yet. Say something.</p>
          )}

          {messages.map((m) => (
            <p className="gc-line" key={m.id}>
              <span className="gc-sender">{m.sender}:</span>
              <span className="gc-text">{m.text}</span>
            </p>
          ))}

          {status === "ended" && endedAt && (
            <p className="gc-system">
              Chat ended at {formatTime(endedAt)} · {messages.length}{" "}
              {messages.length === 1 ? "message" : "messages"} saved
            </p>
          )}
        </div>

        <form className="gc-form" onSubmit={sendMessage}>
          <input
            ref={inputRef}
            className="gc-input"
            type="text"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder={isActive ? "Type a message" : "Start the chat to type"}
            disabled={!isActive}
            autoComplete="off"
            aria-label="Message"
          />
          <button
            type="submit"
            className="gc-btn gc-btn-send"
            disabled={!isActive || draft.trim().length === 0 || disableSubmit}
          >
            Send
          </button>
        </form>
      </section>

      {status === "ended" && (
        <div>If there is issues, LLM output is here</div>
      )}
    </>
  );
}