import { useRef, MouseEvent } from "react";
import MovieCard from "../MovieCard/MovieCard.tsx";
import { Movie } from "../../types/Movie.ts";
import { Handlers } from "../../types/Handlers.ts";
import "./Slider.css";

interface Props {
  title: string;
  movies: Movie[];
  handlers: Handlers;
}

function Slider({ title, movies, handlers }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);

  let isDown: boolean = false;
  let startX: number = 0;
  let scrollLeft: number = 0;

  const handleMouseDown = (event: MouseEvent<HTMLDivElement>) => {
    if (!scrollRef.current) return;
    isDown = true;
    scrollRef.current.classList.add("active");
    startX = event.pageX - scrollRef.current.offsetLeft;
    scrollLeft = scrollRef.current.scrollLeft;
  };

  const handleMouseLeave = () => {
    if (!scrollRef.current) return;
    isDown = false;
    scrollRef.current.classList.remove("active");
  };

  const handleMouseUp = () => {
    if (!scrollRef.current) return;
    isDown = false;
    scrollRef.current.classList.remove("active");
  };

  const handleMouseMove = (event: MouseEvent<HTMLDivElement>) => {
    if (!scrollRef.current || !isDown) return;
    event.preventDefault();
    const endX = event.pageX - scrollRef.current.offsetLeft;
    const walk = (endX - startX) * 2;
    scrollRef.current.scrollLeft = scrollLeft - walk;
  };

  if (movies.length == 0) return null;

  return (
    <div className="slider-container">
      <h2 className="slider-title">{title}</h2>
      <div
        className="slider"
        ref={scrollRef}
        onMouseDown={handleMouseDown}
        onMouseLeave={handleMouseLeave}
        onMouseUp={handleMouseUp}
        onMouseMove={handleMouseMove}
      >
        {movies.map((movie: Movie) => (
          <div key={movie.title} className="slide-card">
            <MovieCard movie={movie} handlers={handlers} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default Slider;
