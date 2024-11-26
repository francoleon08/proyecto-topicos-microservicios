import "./Stars.css";

const MAX_RATING = 10;

interface Props {
  rating: number;
}

function Stars({ rating }: Props) {
  return (
    <span className="stars">
      {"★".repeat(rating) + "☆".repeat(MAX_RATING - rating)}
    </span>
  );
}

export default Stars;
