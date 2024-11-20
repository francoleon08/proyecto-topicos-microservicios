import { useState } from "react";
import "./Like.css";

interface Props {
  handleClick: () => void;
}

function Like({ handleClick }: Props) {
  const [liked, setLiked] = useState(false);

  return (
    <button
      onClick={() => {
        handleClick();
        setLiked(!liked);
      }}
    >
      <span>{liked ? "♥" : "♡"}</span>
    </button>
  );
}

export default Like;
