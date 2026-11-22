import { useRef, useState, type FormEvent } from "react";
import { searchGames } from "./api";
import type { Game } from "./gameTypes";

type GameSearchProps = {
  label: string;
  placeholder: string;
  onAdd: (game: Game) => void;
  existingGames?: Game[];
  compact?: boolean;
  className?: string;
};

export default function GameSearch({
  label,
  placeholder,
  onAdd,
  existingGames = [],
  compact = false,
  className = "",
}: GameSearchProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Game[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);
  const [unavailableCovers, setUnavailableCovers] = useState<Set<number>>(() => new Set());
  const requestId = useRef(0);
  const existingIds = new Set(existingGames.map(game => game.id));

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedQuery = query.trim();
    if (!trimmedQuery) return;

    const currentRequestId = ++requestId.current;
    setLoading(true);
    setError("");
    setResults([]);
    setUnavailableCovers(new Set());
    setSearched(true);

    try {
      const games = await searchGames(trimmedQuery);
      if (currentRequestId === requestId.current) setResults(games);
    } catch (searchError) {
      if (currentRequestId === requestId.current) {
        setError(searchError instanceof Error ? searchError.message : "Game search failed. Please try again.");
      }
    } finally {
      if (currentRequestId === requestId.current) setLoading(false);
    }
  }

  return (
    <div className={`game-search ${compact ? "compact-game-search" : ""} ${className}`.trim()}>
      <form className={compact ? "search" : "big-search"} onSubmit={handleSubmit}>
        <svg
          aria-hidden="true"
          width={compact ? 18 : 22}
          height={compact ? 18 : 22}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="11" cy="11" r="7" />
          <path d="m20 20-4-4" />
        </svg>
        <input
          aria-label={label}
          autoComplete="off"
          value={query}
          onChange={event => setQuery(event.target.value)}
          placeholder={placeholder}
        />
        {compact ? (
          <button type="submit" className="search-submit" aria-label="Search">
            Search
          </button>
        ) : (
          <button className="primary" type="submit" disabled={loading || !query.trim()}>
            {loading ? "Searching..." : "Search"}
          </button>
        )}
      </form>

      <div className={`igdb-results ${compact ? "compact-results" : ""}`} aria-live="polite">
        {loading && <p className="igdb-message">Searching IGDB...</p>}
        {!loading && error && <p className="igdb-message igdb-error">{error}</p>}
        {!loading && !error && searched && results.length === 0 && (
          <p className="igdb-message">No games found. Try another title.</p>
        )}
        {!loading && results.length > 0 && (
          <div className="igdb-result-grid">
            {results.map(game => {
              const inLibrary = existingIds.has(game.id);
              return (
                <article className="igdb-result" key={game.id}>
                  {game.image && !unavailableCovers.has(game.id) ? (
                    <img
                      src={game.image}
                      alt={`${game.title} cover art`}
                      onError={() =>
                        setUnavailableCovers(current => new Set(current).add(game.id))
                      }
                    />
                  ) : (
                    <div className="cover-unavailable" role="img" aria-label={`${game.title}: cover art unavailable`}>
                      Cover art unavailable
                    </div>
                  )}
                  <div className="igdb-result-info">
                    <span>{game.genre} · {game.platform}</span>
                    <h3>{game.title}</h3>
                    {game.score !== undefined && <p>IGDB rating · {game.score}/5</p>}
                    <button
                      className="secondary"
                      type="button"
                      disabled={inLibrary}
                      aria-label={inLibrary ? `${game.title} is in your library` : `Add ${game.title}`}
                      onClick={() => onAdd(game)}
                    >
                      {inLibrary ? "In library" : "Add"}
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
