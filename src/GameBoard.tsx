import { useState } from "react";
import { gameStatuses, type Game, type GameStatus } from "./gameTypes";

type GameBoardProps = {
  games: Game[];
  catalogGames: Game[];
  onAdd: (game: Game, status: GameStatus) => void;
  onMove: (id: number, status: GameStatus) => void;
  onRemove: (id: number) => void;
};

export default function GameBoard({ games, catalogGames, onAdd, onMove, onRemove }: GameBoardProps) {
  const [addingTo, setAddingTo] = useState<GameStatus | null>(null);

  return (
    <section className="board" aria-label="Game lists">
      {gameStatuses.map(status => {
        const listGames = games.filter(game => game.status === status);
        const availableGames = catalogGames.filter(
          game => !games.some(libraryGame => libraryGame.id === game.id),
        );

        return (
          <div className="board-column" key={status}>
            <div className="board-column-heading">
              <h3>{status}</h3>
              <span>{listGames.length}</span>
            </div>
            <button
              className="board-add-button"
              type="button"
              aria-expanded={addingTo === status}
              aria-label={`Add game to ${status}`}
              onClick={() => setAddingTo(addingTo === status ? null : status)}
            >
              + Add game
            </button>
            {addingTo === status && (
              <div className="board-add-options" aria-label={`Available games for ${status}`}>
                {availableGames.length > 0 ? (
                  availableGames.map(game => (
                    <button
                      type="button"
                      key={game.id}
                      onClick={() => {
                        onAdd(game, status);
                        setAddingTo(null);
                      }}
                    >
                      <img src={game.image} alt="" />
                      <span>{game.title}</span>
                    </button>
                  ))
                ) : (
                  <p>All placeholder games are already in your library.</p>
                )}
              </div>
            )}
            {listGames.map(game => (
              <article key={game.id}>
                <img src={game.image} alt="" />
                <div>
                  <b>{game.title}</b>
                  <small>
                    {game.platform} · {game.hours}h
                  </small>
                  <select
                    aria-label={`Move ${game.title}`}
                    value={game.status}
                    onChange={event => {
                      const nextStatus = gameStatuses.find(option => option === event.target.value);
                      if (nextStatus) onMove(game.id, nextStatus);
                    }}
                  >
                    {gameStatuses.map(option => (
                      <option key={option}>{option}</option>
                    ))}
                  </select>
                  <button
                    className="board-remove-button"
                    type="button"
                    aria-label={`Remove ${game.title}`}
                    onClick={() => onRemove(game.id)}
                  >
                    Remove
                  </button>
                </div>
              </article>
            ))}
          </div>
        );
      })}
    </section>
  );
}
