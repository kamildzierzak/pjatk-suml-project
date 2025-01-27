import { useAuth0 } from "@auth0/auth0-react";
import { useEffect, useState } from "react";
import LogoutButton from "../components/LogoutButton";
import Spinner from "../components/Spinner";

const Dashboard = () => {
  const { user, isAuthenticated, isLoading } = useAuth0();
  const BASE_URL = "https://pjatk-suml-project-backend.onrender.com/api";
  // const BASE_URL = "http://127.0.0.1:5000/api";

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [predictionResult, setPredictionResult] = useState("");
  const [predictionLoading, setPredictionLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      fetchHistory();
    }
  }, [isAuthenticated]);

  // To avoid memory leaks
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  if (isLoading) {
    return <Spinner />;
  }

  if (!isAuthenticated) {
    return (
      <p>
        Nie masz dostępu. <a href="/">Wróć do strony głównej</a>
      </p>
    );
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (file && file.type.startsWith("image/")) {
      setSelectedFile(file);
      const objectUrl = URL.createObjectURL(file);
      setPreviewUrl(objectUrl);
    } else {
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  };

  const handlePredict = async (e) => {
    e.preventDefault();

    if (!selectedFile) return;

    try {
      setPredictionLoading(true);
      setPredictionResult("");

      const formData = new FormData();
      formData.append("image", selectedFile);
      formData.append("user_id", user.sub);
      formData.append("model_id", "cnn");

      const res = await fetch(`${BASE_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (data.label) {
        setPredictionResult({ label: data.label, confidence: data.confidence });
      } else {
        setPredictionResult({
          label: "Brak wyniku",
          confidence: "100",
        });
      }

      fetchHistory();
    } catch (err) {
      console.error(err);
      setPredictionResult("Błąd podczas predykcji");
    } finally {
      setPredictionLoading(false);
    }
  };

  const fetchHistory = async () => {
    setLoadingHistory(true);

    try {
      const res = await fetch(`${BASE_URL}/history?user_id=${user.sub}`);
      const data = await res.json();
      setHistory(data);
      // setHistory(mockHistory);
    } catch (err) {
      console.error(err);
    }
    setLoadingHistory(false);
  };

  const handleDelete = async (id) => {
    try {
      await fetch(`${BASE_URL}/history/${id}`, {
        method: "DELETE",
      });
      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col">
      {/* Nav */}
      <div className="mx-auto flex w-full max-w-[768px] flex-row items-center justify-between gap-4 border-b-2 border-blue-700 p-4">
        <h1 className="w-fit text-base sm:text-xl">
          Witaj,{" "}
          <span className="font-semibold text-blue-700">{user.name}</span>.
        </h1>
        <LogoutButton />
      </div>

      {/* Content */}
      <div className="mx-auto flex w-full max-w-[768px] flex-col py-4">
        {/* Prediction section */}
        <div className="mb-4 flex flex-col p-4">
          <h2 className="mb-2 border-b-2 text-lg font-semibold uppercase">
            Predykcja
          </h2>
          <form className="flex flex-col px-2 pb-2" onSubmit={handlePredict}>
            <div className="mb-2">
              <label
                className="block py-2 font-semibold uppercase"
                htmlFor="file"
              >
                Wgraj zdjęcie (jpg, jpeg, png)
              </label>
              <input
                className="w-full rounded bg-green-500 font-semibold file:mr-4 file:bg-blue-500 file:p-2 file:text-white hover:cursor-pointer hover:bg-blue-700 hover:text-blue-700 hover:file:cursor-pointer hover:file:bg-blue-700 sm:w-[360px]"
                type="file"
                id="file"
                name="file"
                accept="image/jpeg, image/png"
                onChange={handleFileChange}
              />
            </div>
            {previewUrl && (
              <div className="mb-2">
                <h3 className="py-2 font-semibold uppercase">
                  Podgląd zdjęcia
                </h3>
                <img
                  className="max-w-[360px] object-contain"
                  src={previewUrl}
                  alt="Podgląd wybranego zdjecia"
                />
              </div>
            )}
            {selectedFile && (
              <button
                type="submit"
                className="rounded-md bg-green-500 p-2 font-semibold text-white hover:bg-green-700 sm:w-[360px]"
              >
                Przewiduj
              </button>
            )}
          </form>
          {(predictionLoading || predictionResult.label) && (
            <div className="px-2">
              <h3 className="py-2 font-semibold uppercase">Wynik</h3>
              {predictionLoading ? (
                <p className="rounded border-2 p-2 text-center font-bold sm:w-[360px]">
                  Hmm...
                </p>
              ) : (
                <p className="rounded border-2 p-2 text-center font-bold sm:w-[360px]">
                  {predictionResult.label} (
                  {Number(predictionResult.confidence).toFixed(3)}%)
                </p>
              )}
            </div>
          )}
        </div>

        {/* History */}
        <div className="mb-4 flex max-w-[768px] flex-col p-4">
          <h2 className="mb-2 border-b-2 text-lg font-semibold uppercase">
            Historia
          </h2>
          {loadingHistory ? (
            <div className="px-2">Ładowanie historii...</div>
          ) : (
            <div className="w-full overflow-x-auto px-2">
              <ul className="flex min-w-[375px] flex-col gap-2 text-xs sm:text-base">
                <li className="grid grid-cols-10 place-items-center border-b border-dashed py-2">
                  <span className="col-span-1 font-semibold">Id</span>
                  <span className="col-span-2 font-semibold">Zdjęcie</span>
                  <span className="col-span-3 font-semibold">Data</span>
                  <span className="col-span-2 font-semibold">Wynik</span>
                  <span className="col-span-2 font-semibold">Akcje</span>
                </li>
                {history.length === 0 ? (
                  <div className="py-2 text-center">Brak historii.</div>
                ) : (
                  history.map((item) => (
                    <li
                      key={item.id}
                      className="grid grid-cols-10 place-items-center items-center border-b border-dashed py-2"
                    >
                      <span className="col-span-1">{item.id}</span>
                      <img
                        src={item.file_url}
                        alt={item.filename}
                        className="col-span-2 h-16 w-16 object-cover"
                      />
                      <span className="col-span-3 text-center">
                        {new Date(item.created_at).toLocaleString()}
                      </span>
                      <span className="col-span-2">{item.label}</span>
                      <span className="col-span-2">
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="rounded bg-red-500 p-2 text-white hover:cursor-pointer hover:bg-red-700"
                        >
                          Usuń
                        </button>
                      </span>
                    </li>
                  ))
                )}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
