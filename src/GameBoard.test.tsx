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
      onMove={(id, status) =>
        setGames(current =>
          current.map(game =>
            game.id === id
              ? { ...game, status, progress: status === "Completed" ? 100 : game.progress }
              : game,
          ),
        )
      }
      onRemove={id => setGames(current => current.filter(game => game.id !== id))}
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
          onRemove={() => {}}
        />
      );
    }

    render(<BoardWithCatalogGameAlreadyAdded />);
    fireEvent.click(screen.getByRole("button", { name: "Add game to Backlog" }));

    expect(screen.queryByRole("button", { name: "Neon Drifter" })).toBeNull();
    expect(screen.getByText("All placeholder games are already in your library.")).toBeTruthy();
  });

  it("moves a game to another list and updates both list counts", () => {
    render(<StatefulGameBoard />);

    fireEvent.change(screen.getByRole("combobox", { name: "Move Echoes of Orion" }), {
      target: { value: "Backlog" },
    });

    const playingHeading = screen.getByRole("heading", { name: "Playing" });
    const playingColumn = playingHeading.parentElement?.parentElement;
    const backlogHeading = screen.getByRole("heading", { name: "Backlog" });
    const backlogColumn = backlogHeading.parentElement?.parentElement;
    if (!playingColumn || !backlogColumn) throw new Error("Game lists were not rendered");

    expect(within(playingColumn).queryByText("Echoes of Orion")).toBeNull();
    expect(within(playingColumn).getByText("0")).toBeTruthy();
    expect(within(backlogColumn).getByText("Echoes of Orion")).toBeTruthy();
    expect(within(backlogColumn).getByText("1")).toBeTruthy();
  });

  it("removes a game from its list and updates the list count", () => {
    render(<StatefulGameBoard />);

    fireEvent.click(screen.getByRole("button", { name: "Remove Echoes of Orion" }));

    const playingHeading = screen.getByRole("heading", { name: "Playing" });
    const playingColumn = playingHeading.parentElement?.parentElement;
    if (!playingColumn) throw new Error("Playing list was not rendered");

    expect(within(playingColumn).queryByText("Echoes of Orion")).toBeNull();
    expect(within(playingColumn).getByText("0")).toBeTruthy();
  });
});
