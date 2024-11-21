export interface Movie {
  imdb: {
    id: number;
    rating: number;
    votes: number;
  };
  title: string;
  poster: string;
  plot: string;
  genres: string[];
  year: number;
}
