"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import "./GameChat.css";

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

export interface ChatMessage {
  id: string;
  sender: string;
  text: string;
  timestamp: string; // ISO string
}

export interface ChatSession {
  id: string;
  startedAt: string; // ISO string
  endedAt: string; // ISO string
  messages: ChatMessage[];
}

type ChatStatus = "idle" | "active" | "ended";

interface GameChatProps {
  /** Name shown next to the user's messages. */
  playerName?: string;
  /** Called once when the user ends the chat, with the full history. */
  onEnd?: (session: ChatSession) => void;
  /** Max characters per message. */
  maxLength?: number;
}

/* ------------------------------------------------------------------ */
/* Storage helpers: ended chats are kept in localStorage until sent   */
/* ------------------------------------------------------------------ */

const STORAGE_KEY = "game-chat:pending-sessions";

export function getPendingSessions(): ChatSession[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as ChatSession[]) : [];
  } catch {
    return [];
  }
}

function savePendingSession(session: ChatSession): void {
  try {
    const all = getPendingSessions();
    all.push(session);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
  } catch {
    // Storage full or unavailable: the onEnd callback still receives the data.
  }
}

/**
 * Call this whenever you are ready to upload (e.g. on a button click or
 * a timer). Sessions are removed from storage only after a successful send.
 */
export async function sendPendingSessions(endpoint: string): Promise<boolean> {
  const sessions = getPendingSessions();
  if (sessions.length === 0) return true;

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sessions }),
    });
    if (!res.ok) return false;
    localStorage.removeItem(STORAGE_KEY);
    return true;
  } catch {
    return false;
  }
}

/* ------------------------------------------------------------------ */
/* Utilities                                                           */
/* ------------------------------------------------------------------ */

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

/* ------------------------------------------------------------------ */
/* Component                                                           */
/* ------------------------------------------------------------------ */

export default function GameChat({
  playerName = "You",
  onEnd,
  maxLength = 200,
}: GameChatProps) {
  const [status, setStatus] = useState<ChatStatus>("idle");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [startedAt, setStartedAt] = useState<string | null>(null);
  const [endedAt, setEndedAt] = useState<string | null>(null);

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

    const ended = new Date().toISOString();
    const session: ChatSession = {
      id: makeId(),
      startedAt,
      endedAt: ended,
      messages,
    };

    savePendingSession(session);
    onEnd?.(session);
    setEndedAt(ended);
    setStatus("ended");
  };

  const sendMessage = (e: FormEvent) => {
    e.preventDefault();
    const text = draft.trim();
    if (!text || status !== "active") return;

    setMessages((prev) => [
      ...prev,
      {
        id: makeId(),
        sender: playerName,
        text,
        timestamp: new Date().toISOString(),
      },
    ]);
    setDraft("");
  };

  const isActive = status === "active";

  return (
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
            <time className="gc-time" dateTime={m.timestamp}>
              {formatTime(m.timestamp)}
            </time>
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
          maxLength={maxLength}
          placeholder={isActive ? "Type a message" : "Start the chat to type"}
          disabled={!isActive}
          autoComplete="off"
          aria-label="Message"
        />
        <button
          type="submit"
          className="gc-btn gc-btn-send"
          disabled={!isActive || draft.trim().length === 0}
        >
          Send
        </button>
      </form>
    </section>
  );
}