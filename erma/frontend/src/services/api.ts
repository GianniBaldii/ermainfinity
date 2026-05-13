import type { ErmaResponse, ErmaState } from "../types/erma";

const API_URL = "http://127.0.0.1:8000";

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

export async function wakeErma(): Promise<ErmaResponse> {
  const response = await fetch(`${API_URL}/wake`, { method: "POST" });
  return parseResponse<ErmaResponse>(response);
}

export async function sleepErma(): Promise<ErmaResponse> {
  const response = await fetch(`${API_URL}/sleep`, { method: "POST" });
  return parseResponse<ErmaResponse>(response);
}
