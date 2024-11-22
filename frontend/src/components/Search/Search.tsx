import { Handlers } from "../../types/Handlers.ts";
import "./Search.css";

interface Props {
  handlers: Handlers;
}

function Search({ handlers }: Props) {
  const handleKeyPress = (event: React.ChangeEvent<HTMLInputElement>) => {
    const search = event.target.value;
    handlers.searchMovie(search);
  };

  return (
    <search id="searchbar">
      <span id="icon">&#9906;</span>
      <input
        onChange={handleKeyPress}
        id="input"
        placeholder="Search for a Movie"
      />
    </search>
  );
}

export default Search;
