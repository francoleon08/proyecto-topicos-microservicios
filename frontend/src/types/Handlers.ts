import { Movie } from "./Movie.ts";

export interface Handlers {
  addMovie: (movie: Movie) => void;
}
