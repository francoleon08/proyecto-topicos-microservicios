import React from "react";
import { Movie } from "../types/Movie.ts";

export const addMovie = (
  setMovies: React.Dispatch<React.SetStateAction<Movie[]>>,
) => {
  return (movie: Movie) => {
    setMovies((movies: Movie[]) => {
      const exists = movies.some((prev) => prev.imdb.id === movie.imdb.id);
      return exists ? movies : [movie, ...movies];
    });
  };
};

export const getRecommendation = async () => {
  const URL_RECOMMENDATIONS =
    import.meta.env.VITE_URL_PROXY + "/movie/recommendation";
  let data: object = {};
  await fetch(URL_RECOMMENDATIONS)
    .then(async (response) => {
      if (!response.ok)
        console.log(`There was an error fetching data: ${response.status}`);
      else data = await response.json();
    })
    .catch((error) => {
      console.log(error.message);
    });
  return Object.keys(data).length === 0 ? null : (data as Movie);
};
