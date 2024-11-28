import { useEffect, useState } from "react";
import Info from "./components/Info/Info.tsx";
import Search from "./components/Search/Search.tsx";
import User from "./components/User/User.tsx";
import Theme from "./components/Theme/Theme.tsx";
import Slider from "./components/Slider/Slider.tsx";
import useFetch from "./hooks/useFetch.ts";
import { addMovie, getRecommendation, searchMovie } from "./utils/utils.ts";
import { Movie } from "./types/Movie.ts";
import { Handlers } from "./types/Handlers.ts";
import "./App.css";

const VITE_URL_RANDOM_MOVIES = import.meta.env.VITE_URL_RANDOM_MOVIES;
const VITE_URL_HISTORY = import.meta.env.VITE_URL_HISTORY;
const CLICKS_COUNT = Number(import.meta.env.VITE_CLICKS_COUNT);

const URL_RANDOM_MOVIES = VITE_URL_RANDOM_MOVIES + "/randommovies?limit=30";
const URL_HISTORY = VITE_URL_HISTORY + "/history/allHistory";

function App() {
  const {
    data: movies,
    loading: loadingMovies,
    error: errorMovies,
  } = useFetch<Movie[]>(URL_RANDOM_MOVIES);

  const {
    data: loadedForyou,
    loading: loadingForyou,
    error: errorForyou,
  } = useFetch<Movie[]>(URL_RANDOM_MOVIES);

  const {
    data: loadedHistory,
    loading: loadingHistory,
    error: errorHistory,
  } = useFetch<Movie[]>(URL_HISTORY);

  const error = errorMovies || errorForyou || errorHistory;
  const loading = loadingMovies || loadingForyou || loadingHistory;

  const [search, setSearch] = useState<Movie[]>([]);
  const [history, setHistory] = useState<Movie[]>([]);
  const [foryou, setForyou] = useState<Movie[]>([]);
  const [clicks, setClicks] = useState(0);

  const handlers: Handlers = {
    addMovieToHistory: addMovie(setHistory),
    registerClick: () => setClicks(clicks + 1),
    searchMovie: async (search: string) =>
      searchMovie(search).then((movies: Movie[]) => {
        const uniqueMovies = movies?.filter(
          (movie, index, self) =>
            index === self.findIndex((m) => m.title === movie.title)
        );
        setSearch(uniqueMovies ?? []);
      }),    
  };

  useEffect(() => {
    if (loadedHistory) setHistory(loadedHistory);
  }, [loadedHistory]);

  useEffect(() => {
    if (loadedForyou) setForyou(loadedForyou);
  }, [loadedForyou]);

  useEffect(() => {
    if (clicks === CLICKS_COUNT) {
      setClicks(0);
      getRecommendation().then((movie: Movie | null) => {
        if (movie) addMovie(setForyou)(movie);
      });
    }
  }, [clicks]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div id="app">
      <header>
        <Info title="DCICFLIX" />
        <div>
          <Search handlers={handlers} />
          <User />
          <Theme />
        </div>
      </header>
      <main>
        <Slider title="Search" movies={search ?? []} handlers={handlers} />
        <Slider title="For You" movies={foryou ?? []} handlers={handlers} />
        <Slider title="Upcoming" movies={movies ?? []} handlers={handlers} />
        <Slider title="History" movies={history ?? []} handlers={handlers} />
      </main>
    </div>
  );
}

export default App;
