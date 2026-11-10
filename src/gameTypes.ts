export const gameStatuses = ["Playing", "Backlog", "Completed", "On hold"] as const;
export type GameStatus = (typeof gameStatuses)[number];

export type Game = {
  id: number;
  title: string;
  genre: string;
  platform: string;
  progress: number;
  hours: number;
  status: GameStatus;
  image: string;
  color: string;
  score?: number;
};
