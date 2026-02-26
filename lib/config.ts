export type Difficulty = "easy" | "medium" | "difficult";

export const DIFFICULTY_OPTIONS: Difficulty[] = ["easy", "medium", "difficult"];
export const DEFAULT_DIFFICULTY: Difficulty = "easy";

const DEFAULT_MODEL_BY_DIFFICULTY: Record<Difficulty, string> = {
  easy:
    "Qwen/Qwen2.5-1.5B-Instruct:featherless-ai",
  medium: "ruslandev/llama-3-8b-gpt-4o-ru1.0:featherless-ai",
  difficult: "openai/gpt-oss-20b:groq",
};

export function sanitizeDifficulty(value: unknown): Difficulty {
  if (value === "easy" || value === "medium" || value === "difficult") {
    return value;
  }
  return DEFAULT_DIFFICULTY;
}

export function getClientModelByDifficulty(): Record<Difficulty, string> {
  return {
    easy:
      process.env.NEXT_PUBLIC_HF_MODEL_EASY ??
      process.env.NEXT_PUBLIC_HF_MODEL ??
      DEFAULT_MODEL_BY_DIFFICULTY.easy,
    medium:
      process.env.NEXT_PUBLIC_HF_MODEL_MEDIUM ??
      DEFAULT_MODEL_BY_DIFFICULTY.medium,
    difficult:
      process.env.NEXT_PUBLIC_HF_MODEL_DIFFICULT ??
      DEFAULT_MODEL_BY_DIFFICULTY.difficult,
  };
}

export function getServerModelByDifficulty(): Record<Difficulty, string> {
  return {
    easy:
      process.env.HF_MODEL_EASY ??
      process.env.HF_MODEL ??
      process.env.NEXT_PUBLIC_HF_MODEL_EASY ??
      process.env.NEXT_PUBLIC_HF_MODEL ??
      DEFAULT_MODEL_BY_DIFFICULTY.easy,
    medium:
      process.env.HF_MODEL_MEDIUM ??
      process.env.NEXT_PUBLIC_HF_MODEL_MEDIUM ??
      DEFAULT_MODEL_BY_DIFFICULTY.medium,
    difficult:
      process.env.HF_MODEL_DIFFICULT ??
      process.env.NEXT_PUBLIC_HF_MODEL_DIFFICULT ??
      DEFAULT_MODEL_BY_DIFFICULTY.difficult,
  };
}
