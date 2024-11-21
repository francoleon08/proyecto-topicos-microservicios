import { Movie } from "../../types/Movie.ts";

const HISTORY_URL = import.meta.env.VITE_URL_HISTORY + "/history";
const PROXY_URL = import.meta.env.VITE_URL_PROXY + "/movie/viewed";

export const addToHistory = (movie: Movie) => {
  sendPost(
    HISTORY_URL,
    JSON.stringify({
      imdb: movie.imdb,
      title: movie.title,
      poster: movie.poster,
      plot: movie.plot,
    }),
  );
};

export const registerLike = (movie: Movie) => {
  sendPost(
    PROXY_URL,
    JSON.stringify({
      imdb: movie.imdb,
      title: movie.title,
      poster: movie.poster,
      plot: movie.plot,
      genres: movie.genres,
      year: movie.year,
    }),
  );
};

export const sendPost = async (url: string, body: BodyInit) => {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body,
    });
    if (!response.ok) console.error("Response Error: ", response.statusText);
  } catch (error) {
    console.error("Connection Error: ", error);
  }
};
