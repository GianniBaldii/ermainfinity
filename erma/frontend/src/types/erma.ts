export type ErmaStatus =
  | "idle"
  | "listening"
  | "thinking"
  | "talking"
  | "sleep"
  | "greeting";

export type ErmaEmotion = "neutral" | "alegre" | "cansado" | "curioso";

export type ErmaState = {
  status: ErmaStatus;
  emotion: ErmaEmotion;
  message: string;
};

export type ErmaResponse = ErmaState & {
  intent: string;
  matched_keywords: string[];
};

export type ErmaHistoryEntry = ErmaResponse & {
  timestamp: string;
  command: string;
};

export type ErmaNote = {
  id: number;
  text: string;
  created_at: string;
};
