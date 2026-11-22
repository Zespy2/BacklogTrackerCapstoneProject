// Helpers for talking to the Django backend (backend/accounts/views.py).
// In development, Vite forwards every request that starts with /api to
// Django at http://127.0.0.1:8000 (see the "proxy" setting in vite.config.ts).
import { gameStatuses, type Game } from "./gameTypes";

export type User = { id: number; username: string; email: string };

function isGame(value: unknown): value is Game {
  if (typeof value !== "object" || value === null) return false;
  const game = value as Record<string, unknown>;
  return (
    typeof game.id === "number" &&
    typeof game.title === "string" &&
    typeof game.genre === "string" &&
    typeof game.platform === "string" &&
    typeof game.progress === "number" &&
    typeof game.hours === "number" &&
    gameStatuses.some(status => status === game.status) &&
    typeof game.image === "string" &&
    typeof game.color === "string" &&
    (game.score === undefined || typeof game.score === "number")
  );
}

export async function searchGames(query: string): Promise<Game[]> {
  const response = await fetch(`/api/games/search/?q=${encodeURIComponent(query)}`, {
    credentials: "same-origin",
  });
  const data: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    const message =
      typeof data === "object" &&
      data !== null &&
      "error" in data &&
      typeof data.error === "string"
        ? data.error
        : "Game search failed. Please try again.";
    throw new Error(message);
  }

  if (
    typeof data !== "object" ||
    data === null ||
    !("games" in data) ||
    !Array.isArray(data.games) ||
    !data.games.every(isGame)
  ) {
    throw new Error("Game search returned an invalid response. Please try again.");
  }

  return data.games;
}

// Django sends the CSRF token as a cookie; we copy it into a header on POSTs.
function getCookie(name: string): string {
  const match = document.cookie.split("; ").find(row => row.startsWith(name + "="));
  return match ? decodeURIComponent(match.split("=")[1]) : "";
}

async function ensureCsrfCookie() {
  if (!getCookie("csrftoken")) await fetch("/api/csrf/", { credentials: "same-origin" });
}

async function post(path: string, body: object = {}): Promise<{ user?: User | null }> {
  await ensureCsrfCookie();
  let response: Response;
  try {
    response = await fetch(path, {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
      body: JSON.stringify(body),
    });
  } catch {
    throw new Error("Can't reach the server. Is Django running?");
  }
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    if (response.status === 403) throw new Error("Security check failed. Refresh the page and try again.");
    throw new Error(data.error || "Can't reach the server. Is Django running?");
  }
  return data;
}

/** Who is signed in right now (null if nobody, or if Django isn't running). */
export async function getCurrentUser(): Promise<User | null> {
  try {
    const response = await fetch("/api/me/", { credentials: "same-origin" });
    if (!response.ok) return null;
    const data = await response.json();
    return data.user ?? null;
  } catch {
    return null;
  }
}

export async function signUp(email: string, password: string, username: string): Promise<User> {
  const data = await post("/api/signup/", { email, password, username });
  return data.user as User;
}

export async function signIn(email: string, password: string): Promise<User> {
  const data = await post("/api/login/", { email, password });
  return data.user as User;
}

export async function signOut(): Promise<void> {
  await post("/api/logout/");
}

export async function deleteAccount(password: string): Promise<void> {
  await post("/api/delete-account/", { password });
}