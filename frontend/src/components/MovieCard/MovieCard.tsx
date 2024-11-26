import { useEffect, useState } from "react";
import { Card } from "react-bootstrap";
import Stars from "../Stars/Stars.tsx";
import Like from "../Like/Like.tsx";
import { Movie } from "../../types/Movie.ts";
import { Handlers } from "../../types/Handlers.ts";
import { addToHistory, registerLike } from "./MovieService.ts";
import "./MovieCard.css";

const IMAGE_SIZE = { width: 300, height: 400 };

interface Props {
  movie: Movie;
  handlers: Handlers;
}

function MovieCard({ movie, handlers }: Props) {
  const [visible, setVisible] = useState(true);

  const handleClick = () => {
    handlers.addMovieToHistory(movie);
    handlers.registerClick(movie);
    addToHistory(movie);
    registerLike(movie);
  };

  useEffect(() => {
    hasPoster(movie.poster).then((has) => {
      if (!has) setVisible(false);
      else {
        const img = new Image();
        img.onload = () => {
          setVisible(
            img.width >= IMAGE_SIZE.width && img.height >= IMAGE_SIZE.height,
          );
        };
        img.onerror = () => setVisible(false);
        img.src = movie.poster;
      }
    });
  }, [movie.poster]);

  if (!visible) return null;
  hasPoster(movie.poster).then((has) => setVisible(has));

  return (
    <Card className="card-custom">
      <Card.Img variant="top" src={movie.poster} alt={movie.title} />
      <Card.Body>
        <Card.Title className="card-title">{movie.title}</Card.Title>
        <Card.Text className="card-text">{movie.plot}</Card.Text>
        <Stars rating={movie.imdb.rating} />
        <Like handleClick={handleClick} />
      </Card.Body>
    </Card>
  );
}

export default MovieCard;

async function hasPoster(poster: string | null) {
  if (!poster) return false;
  try {
    const response = await fetch(poster, { method: "HEAD" });
    return response.ok;
  } catch {
    return false;
  }
}
