import { Movie } from "./Movie.ts";

export interface Handlers {
  addMovieToHistory: (movie: Movie) => void;
  registerClick: (movie: Movie) => void;
  searchMovie: (search: string) => void;
}
