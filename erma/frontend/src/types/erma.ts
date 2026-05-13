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
