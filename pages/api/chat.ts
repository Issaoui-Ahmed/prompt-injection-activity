import type { NextApiRequest, NextApiResponse } from "next";

import {
  Difficulty,
  getServerModelByDifficulty,
  sanitizeDifficulty,
} from "../../lib/config";

type Turn = {
  prompt: string;
  response: string;
};

type ChatSuccess = {
  response: string;
  modelName: string;
};

type ChatError = {
  error: string;
};

const HF_ROUTER_URL = "https://router.huggingface.co/v1/chat/completions";
const RETRYABLE_STATUS_CODES = new Set([429, 500, 502, 503, 504]);
const MAX_RETRIES = 2;
const REQUEST_TIMEOUT_MS = 45_000;
const RETRY_DELAY_MS = 500;

function normalizeResponseContent(content: unknown): string {
  if (typeof content === "string") {
    return content;
  }
  if (Array.isArray(content)) {
    return content
      .map((item) => {
        if (
          item &&
          typeof item === "object" &&
          "text" in item &&
          typeof item.text === "string"
        ) {
          return item.text;
        }
        return String(item);
      })
      .join("\n");
  }
  return String(content ?? "");
}

function isTurnArray(value: unknown): value is Turn[] {
  if (!Array.isArray(value)) {
    return false;
  }
  return value.every((turn) => {
    if (!turn || typeof turn !== "object") {
      return false;
    }
    return (
      typeof turn.prompt === "string" && typeof turn.response === "string"
    );
  });
}

function buildMessages(fileText: string, turns: Turn[], prompt: string) {
  const messages: Array<{ role: "system" | "user" | "assistant"; content: string }> = [
    { role: "system", content: fileText },
  ];

  for (const turn of turns) {
    messages.push({ role: "user", content: turn.prompt });
    messages.push({ role: "assistant", content: turn.response });
  }

  messages.push({ role: "user", content: prompt });
  return messages;
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function compactWhitespace(value: string): string {
  return value.replace(/\s+/g, " ").trim();
}

function truncate(value: string, maxLength = 240): string {
  if (value.length <= maxLength) {
    return value;
  }
  return `${value.slice(0, maxLength - 1)}...`;
}

function extractJsonError(payload: unknown): string | null {
  if (!payload || typeof payload !== "object") {
    return null;
  }

  const root = payload as Record<string, unknown>;
  if (typeof root.error === "string") {
    return root.error;
  }
  if (typeof root.message === "string") {
    return root.message;
  }
  if (root.error && typeof root.error === "object") {
    const nested = root.error as Record<string, unknown>;
    if (typeof nested.message === "string") {
      return nested.message;
    }
  }
  return null;
}

function looksLikeHtml(body: string, contentType: string): boolean {
  const normalizedType = contentType.toLowerCase();
  return (
    normalizedType.includes("text/html") ||
    /^\s*<!doctype html/i.test(body) ||
    /^\s*<html/i.test(body)
  );
}

function extractHtmlSummary(html: string): string | null {
  const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  if (titleMatch?.[1]) {
    return compactWhitespace(titleMatch[1]);
  }

  const h1Match = html.match(/<h1[^>]*>([^<]+)<\/h1>/i);
  if (h1Match?.[1]) {
    return compactWhitespace(h1Match[1]);
  }

  const pMatch = html.match(/<p[^>]*>([^<]+)<\/p>/i);
  if (pMatch?.[1]) {
    return compactWhitespace(pMatch[1]);
  }

  return null;
}

async function summarizeUpstreamError(upstream: Response): Promise<string> {
  if (upstream.status === 503) {
    return "Hugging Face router is temporarily unavailable (503). Please retry in a few seconds.";
  }

  const statusLine = upstream.statusText
    ? `Hugging Face request failed (${upstream.status} ${upstream.statusText}).`
    : `Hugging Face request failed (${upstream.status}).`;
  const contentType = upstream.headers.get("content-type") ?? "";
  const rawBody = await upstream.text();
  const normalizedBody = compactWhitespace(rawBody);

  if (!normalizedBody) {
    return statusLine;
  }

  if (contentType.toLowerCase().includes("application/json")) {
    try {
      const parsed = JSON.parse(normalizedBody);
      const detail = extractJsonError(parsed);
      if (detail) {
        return `${statusLine} ${truncate(compactWhitespace(detail))}`;
      }
    } catch {
      // Ignore parsing errors and fall back to plain-text handling.
    }
  }

  if (looksLikeHtml(normalizedBody, contentType)) {
    const htmlSummary = extractHtmlSummary(normalizedBody);
    if (htmlSummary) {
      return `${statusLine} ${truncate(htmlSummary)}`;
    }
    return statusLine;
  }

  return `${statusLine} ${truncate(normalizedBody)}`;
}

async function fetchCompletionWithRetry(
  token: string,
  modelName: string,
  messages: Array<{ role: "system" | "user" | "assistant"; content: string }>
): Promise<Response> {
  let lastError: unknown;

  for (let attempt = 0; attempt <= MAX_RETRIES; attempt += 1) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    try {
      const upstream = await fetch(HF_ROUTER_URL, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: modelName,
          messages,
        }),
        signal: controller.signal,
      });

      if (
        !RETRYABLE_STATUS_CODES.has(upstream.status) ||
        attempt === MAX_RETRIES
      ) {
        return upstream;
      }
    } catch (error) {
      lastError = error;
      if (attempt === MAX_RETRIES) {
        throw error;
      }
    } finally {
      clearTimeout(timeoutId);
    }

    await sleep(RETRY_DELAY_MS * (attempt + 1));
  }

  throw (
    lastError ?? new Error("No response returned from the model provider.")
  );
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ChatSuccess | ChatError>
) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed." });
  }

  try {
    const { fileText, prompt, turns, difficulty, hfToken } = req.body ?? {};

    if (typeof fileText !== "string" || !fileText.trim()) {
      return res
        .status(400)
        .json({ error: "Missing or invalid fileText in request body." });
    }
    if (typeof prompt !== "string" || !prompt.trim()) {
      return res
        .status(400)
        .json({ error: "Missing or invalid prompt in request body." });
    }
    if (!isTurnArray(turns)) {
      return res
        .status(400)
        .json({ error: "Missing or invalid turns in request body." });
    }
    if (typeof hfToken !== "string" || !hfToken.trim()) {
      return res
        .status(400)
        .json({ error: "Missing or invalid hfToken in request body." });
    }
    const safeDifficulty: Difficulty = sanitizeDifficulty(difficulty);
    const modelName = getServerModelByDifficulty()[safeDifficulty];
    const token = hfToken.trim();
    const messages = buildMessages(fileText, turns, prompt);
    const upstream = await fetchCompletionWithRetry(token, modelName, messages);

    if (!upstream.ok) {
      const detail = await summarizeUpstreamError(upstream);
      return res.status(upstream.status).json({
        error: `Inference failed: ${detail}`,
      });
    }

    const completion = await upstream.json();
    const content = completion?.choices?.[0]?.message?.content;

    return res.status(200).json({
      response: normalizeResponseContent(content),
      modelName,
    });
  } catch (error) {
    const message =
      error instanceof Error
        ? error.name === "AbortError"
          ? "Model request timed out. Please retry."
          : error.message
        : "Unexpected error while calling the model.";
    return res.status(500).json({ error: `Inference failed: ${message}` });
  }
}
