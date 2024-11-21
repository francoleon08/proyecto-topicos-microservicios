import "./Info.css";

interface Props {
  title: string;
}

function Info({ title }: Props) {
  return (
    <div id="info">
      <h1>{title}</h1>
      <img style={{ display: "none" }} src="images/logo.png" alt={title} />
    </div>
  );
}

export default Info;
