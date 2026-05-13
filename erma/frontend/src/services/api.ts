import type { ErmaHistoryEntry, ErmaNote, ErmaResponse, ErmaState } from "../types/erma";

const API_URL = `${window.location.protocol}//${window.location.hostname}:8000`;

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error("ERMA no pudo responder en este momento.");
  }

  return response.json() as Promise<T>;
}

export async function getState(): Promise<ErmaState> {
  const response = await fetch(`${API_URL}/state`);
  return parseResponse<ErmaState>(response);
}

export async function sendCommand(text: string): Promise<ErmaResponse> {
  const response = await fetch(`${API_URL}/command`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  return parseResponse<ErmaResponse>(response);
}

export async function getHistory(): Promise<ErmaHistoryEntry[]> {
  const response = await fetch(`${API_URL}/history?limit=8`);
  return parseResponse<ErmaHistoryEntry[]>(response);
}

export async function getNotes(): Promise<ErmaNote[]> {
  const response = await fetch(`${API_URL}/notes`);
  return parseResponse<ErmaNote[]>(response);
}

export async function wakeErma(): Promise<ErmaResponse> {
  const response = await fetch(`${API_URL}/wake`, { method: "POST" });
  return parseResponse<ErmaResponse>(response);
}

export async function sleepErma(): Promise<ErmaResponse> {
  const response = await fetch(`${API_URL}/sleep`, { method: "POST" });
  return parseResponse<ErmaResponse>(response);
}
