import { cleanup, fireEvent, render, screen } from "@testing-library/react"
import { afterEach, describe, expect, it, vi } from "vitest"
import { FeaturePage } from "./App"
import type { Game } from "./gameTypes"

const catalogGames: Game[] = [
  {
    id: 12,
    title: "Neon Drifter",
    genre: "Racing",
    platform: "PS5",
    progress: 0,
    hours: 0,
    status: "Backlog",
    image: "/drifter.jpg",
    color: "#e84f8a",
  },
  {
    id: 13,
    title: "Hollow Vale",
    genre: "Adventure",
    platform: "PC",
    progress: 0,
    hours: 0,
    status: "Backlog",
    image: "/vale.jpg",
    color: "#489bb8",
  },
]

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe("Add games page", () => {
  it("searches IGDB and adds a matching game", async () => {
    const onAdd = vi.fn()
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ games: [catalogGames[0]] }),
    }))

    render(
      <FeaturePage
        view="Add games"
        games={[]}
        availableGames={catalogGames}
        onAdd={onAdd}
        onRemove={() => {}}
        onMove={() => {}}
        notify={() => {}}
      />,
    )

    fireEvent.change(
      screen.getByRole("textbox", { name: "Search games to add" }),
      {
        target: { value: "racing" },
      },
    )
    fireEvent.click(screen.getByRole("button", { name: "Search" }))

    expect(await screen.findByRole("heading", { name: "Neon Drifter" })).toBeTruthy()
    expect(screen.queryByRole("heading", { name: "Hollow Vale" })).toBeNull()
    expect(fetch).toHaveBeenCalledWith("/api/games/search/?q=racing", {
      credentials: "same-origin",
    })

    fireEvent.error(screen.getByRole("img", { name: "Neon Drifter cover art" }))
    expect(
      screen.getByRole("img", { name: "Neon Drifter: cover art unavailable" }),
    ).toBeTruthy()

    fireEvent.click(    screen.getByRole("button", { name: "Add Neon Drifter" }))
    expect(onAdd).toHaveBeenCalledWith(catalogGames[0])
  })

  it("shows a clear message when IGDB returns no matching games", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ games: [] }),
      }))

    render(
      <FeaturePage
        view="Search"
        games={[]}
        availableGames={[]}
        onAdd={() => {}}
        onRemove={() => {}}
        onMove={() => {}}
        notify={() => {}}
      />,
    )

    fireEvent.change(
      screen.getByRole("textbox", { name: "Search IGDB games" }),
      {
        target: { value: "no matching title" },
      },
    )
    fireEvent.click(screen.getByRole("button", { name: "Search" }))

    expect(
      await screen.findByText("No games found. Try another title."),
    ).toBeTruthy()
  })

  it("shows a clear message when the IGDB request fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ error: "IGDB is not configured." }),
      }))

    render(
      <FeaturePage
        view="Add games"
        games={[]}
        availableGames={[]}
        onAdd={() => {}}
        onRemove={() => {}}
        onMove={() => {}}
        notify={() => {}}
      />,
    )

    fireEvent.change(
      screen.getByRole("textbox", { name: "Search games to add" }),
      {
        target: { value: "zelda" },
      },
    )
    fireEvent.click(screen.getByRole("button", { name: "Search" }))

    expect(await screen.findByText("IGDB is not configured.")).toBeTruthy()
  })
})
