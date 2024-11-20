import { Card } from "react-bootstrap";
import placeholder from "../../assets/images/placeholder.jpg";
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
  const handleClick = () => {
    handlers.addMovie(movie);
    addToHistory(movie);
    registerLike(movie);
  };

  return (
    <Card className="card-custom">
      <Card.Img
        variant="top"
        src={movie.poster || placeholder}
        alt={movie.title}
      />
      <Card.Body>
        <Card.Title className="card-title">{movie.title}</Card.Title>
        <Card.Text className="card-text">{movie.plot}</Card.Text>
        <Like handleClick={handleClick} />
      </Card.Body>
    </Card>
  );
}

export default MovieCard;
