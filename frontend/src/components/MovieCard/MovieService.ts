import { Movie } from "../../types/Movie.ts";

const HISTORY_URL = import.meta.env.VITE_URL_HISTORY + "/history";

export const addToHistory = async (movie: Movie) => {
  try {
    const response = await fetch(HISTORY_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: movie.id,
        imdb: movie.imdb,
        title: movie.title,
        poster: movie.poster,
        plot: movie.plot,
      }),
    });
    if (response.ok) console.log(response);
    else console.error("Response Error: ", response.statusText);
  } catch (error) {
    console.error("Connection Error: ", error);
  }
};

export const registerLike = async (movie: Movie) => {
  console.log(movie);
};
