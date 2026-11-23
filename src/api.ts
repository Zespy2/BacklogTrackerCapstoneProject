// Helpers for talking to the Django backend (backend/accounts/views.py).
// In development, Vite forwards every request that starts with /api to
// Django at http://127.0.0.1:8000 (see the "proxy" setting in vite.config.ts).

export type User = { id: number; username: string; email: string };

// Django sends the CSRF token as a cookie; we copy it into a header on POSTs.
function getCookie(name: string): string {
  const match = document.cookie.split("; ").find(row => row.startsWith(name + "="));
  return match ? decodeURIComponent(match.split("=")[1]) : "";
}

async function ensureCsrfCookie() {
  if (!getCookie("csrftoken")) await fetch("/api/csrf/", { credentials: "same-origin" });
}

async function post(path: string, body: object = {}): Promise<{ user?: User | null; message?: string }> {
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

/** Ask Django to email a password reset link. Returns the message to show. */
export async function requestPasswordReset(email: string): Promise<string> {
  const data = await post("/api/forgot-password/", { email });
  return data.message ?? "If an account uses that email, we've sent a link to reset your password.";
}

/** Set a new password using the uid and token from the reset link. Returns the message to show. */
export async function confirmPasswordReset(uid: string, token: string, newPassword: string): Promise<string> {
  const data = await post("/api/reset-password/", { uid, token, new_password: newPassword });
  return data.message ?? "Your password has been reset. You can sign in now.";
}