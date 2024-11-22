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
        setLiked(!liked);
        if (liked) handleClick();
      }}
    >
      <span>{liked ? "♥" : "♡"}</span>
    </button>
  );
}

export default Like;
