import { Link } from "react-router-dom";

const NotFoundPage = () => {
  return (
    <div className="flex h-screen flex-col items-center justify-center text-center">
      <div className="flex flex-col items-center justify-center sm:rounded-2xl sm:border-2 sm:p-8">
        <h1 className="max-w-[350px] px-4 pb-2 text-3xl font-semibold text-pretty">
          404 - Nie znaleziono
        </h1>
        <p className="max-w-[350px] pb-2 text-xl text-pretty text-neutral-500">
          Strona, której szukasz, nie istnieje lub została przeniesiona.
        </p>
        <Link className="text-2xl text-blue-500 hover:text-blue-700" to="/">
          Wróć na stronę główną
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage;
