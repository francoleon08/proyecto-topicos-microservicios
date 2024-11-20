import { useEffect, useState } from "react";
import Info from "./components/Info/Info.tsx";
import Search from "./components/Search/Search.tsx";
import User from "./components/User/User.tsx";
import Theme from "./components/Theme/Theme.tsx";
import Slider from "./components/Slider/Slider.tsx";
import useFetch from "./hooks/useFetch.ts";
import { Movie } from "./types/Movie.ts";
import { Handlers } from "./types/Handlers.ts";
import "./App.css";

const URL_MOVIES = "http://random-movies:3001/randommovies?limit=30"
const URL_HISTORY = "http://history:8080/history/allHistory"

function App() {
  const {
    data: movies,
    loading: loadingMovies,
    error: errorMovies,
  } = useFetch<Movie[]>(URL_MOVIES);

  const {
    data: foryou,
    loading: loadingForyou,
    error: errorForyou,
  } = useFetch<Movie[]>(URL_MOVIES);

  const {
    data: loadedHistory,
    loading: loadingHistory,
    error: errorHistory,
  } = useFetch<Movie[]>(URL_HISTORY);

  const error = errorMovies || errorForyou || errorHistory;
  const loading = loadingMovies || loadingForyou || loadingHistory;

  const [history, setHistory] = useState<Movie[]>([]);

  const addMovie = (movie: Movie) => {
    setHistory((history: Movie[]) => {
      const exists = history.some((prev: Movie) => prev.imdb === movie.imdb);
      return exists ? history : [movie, ...history];
    });
  };

  const handlers: Handlers = {
    addMovie: addMovie,
  };

  useEffect(() => {
    if (loadedHistory) setHistory(loadedHistory);
  }, [loadedHistory]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div id="app">
      <header>
        <Info title="DCICFLIX" />
        <div>
          <Search />
          <User />
          <Theme />
        </div>
      </header>
      <main>
        <Slider title="For You" movies={foryou ?? []} handlers={handlers} />
        <Slider title="Upcomming" movies={movies ?? []} handlers={handlers} />
        <Slider title="History" movies={history ?? []} handlers={handlers} />
      </main>
    </div>
  );
}

export default App;
