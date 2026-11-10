import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { useState } from "react";
import { afterEach, describe, expect, it } from "vitest";
import GameBoard from "./GameBoard";
import type { Game } from "./gameTypes";

const existingGame: Game = {
  id: 1,
  title: "Echoes of Orion",
  genre: "Sci-fi RPG",
  platform: "PC",
  progress: 68,
  hours: 32,
  status: "Playing",
  image: "/orion.jpg",
  color: "#5d46e8",
};

const catalogGame: Game = {
  id: 12,
  title: "Neon Drifter",
  genre: "Racing",
  platform: "PS5",
  progress: 0,
  hours: 0,
  status: "Backlog",
  image: "/drifter.jpg",
  color: "#e84f8a",
};

afterEach(cleanup);

function StatefulGameBoard() {
  const [games, setGames] = useState([existingGame]);

  return (
    <GameBoard
      games={games}
      catalogGames={[catalogGame]}
      onAdd={(game, status) => setGames(current => [...current, { ...game, status }])}
      onMove={() => {}}
    />
  );
}

describe("GameBoard", () => {
  it("adds a catalog game to the list the user selected", () => {
    render(<StatefulGameBoard />);

    fireEvent.click(screen.getByRole("button", { name: "Add game to Completed" }));
    fireEvent.click(screen.getByRole("button", { name: "Neon Drifter" }));

    const completedHeading = screen.getByRole("heading", { name: "Completed" });
    const completedColumn = completedHeading.parentElement?.parentElement;
    if (!completedColumn) throw new Error("Completed list was not rendered");
    expect(within(completedColumn).getByText("Neon Drifter")).toBeTruthy();
    expect(within(completedColumn).getByText("1")).toBeTruthy();
  });

  it("does not offer games that are already in the library", () => {
    function BoardWithCatalogGameAlreadyAdded() {
      return (
        <GameBoard
          games={[existingGame, catalogGame]}
          catalogGames={[catalogGame]}
          onAdd={() => {}}
          onMove={() => {}}
        />
      );
    }

    render(<BoardWithCatalogGameAlreadyAdded />);
    fireEvent.click(screen.getByRole("button", { name: "Add game to Backlog" }));

    expect(screen.queryByRole("button", { name: "Neon Drifter" })).toBeNull();
    expect(screen.getByText("All placeholder games are already in your library.")).toBeTruthy();
  });
});
