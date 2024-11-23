import { useState } from "react";
import { Card } from "react-bootstrap";
import Like from "../Like/Like.tsx";
import { Movie } from "../../types/Movie.ts";
import { Handlers } from "../../types/Handlers.ts";
import { addToHistory, registerLike } from "./MovieService.ts";
import "./MovieCard.css";

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

  if (!visible) return null;
  hasPoster(movie.poster).then((has) => setVisible(has));

  return (
    <Card className="card-custom">
      <Card.Img variant="top" src={movie.poster} alt={movie.title} />
      <Card.Body>
        <Card.Title className="card-title">{movie.title}</Card.Title>
        <Card.Text className="card-text">{movie.plot}</Card.Text>
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
