import { useState } from "react";
import AnimatedList from "../components/ui/AnimatedList";


function News() {
  const [query, setQuery] = useState("");
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchNews = async () => {
    if (!query.trim()) {
      setError("Please enter a country or keyword.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/news/search?query=${encodeURIComponent(query)}`
      );
      if (!response.ok) throw new Error("Failed to fetch news.");
      const data = await response.json();
      console.log("Fetched data:", data);

      setArticles(Array.isArray(data.data) ? data.data : []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchNews();
  };

 const items = articles.map(a => ({
  title: a.title,
  image: a.urlToImage || a.image || "https://via.placeholder.com/300x200?text=No+Image",
  url: a.url,
  description: a.description
}));

  return (
    <div className="flex flex-col min-h-screen max-w-4xl mx-auto p-6">
  <h1 className="text-3xl font-bold mb-6 text-center text-white">
    Search News by Country
  </h1>

      <form onSubmit={handleSubmit} className="flex gap-2 mb-6 text-white">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter a country name (e.g. Japan, Korea, Indonesia)"
          className="border border-gray-300 p-2 rounded w-full focus:outline-blue-500"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Search
        </button>
      </form>

      {loading && <p className="text-gray-500">Fetching latest news...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {!loading && !error && items.length > 0 && (
        <AnimatedList
          items={items}
          onItemSelect={(item, index) => console.log("Clicked:", item, index)}
          showGradients={true}
          enableArrowNavigation={true}
          displayScrollbar={true}
          className="w-full max-h-screen"
          />
      )}

      {!loading && !error && items.length === 0 && (
        <p className="text-center text-gray-500 mt-8">
          No articles yet — try searching for a country.
        </p>
      )}
    </div>
  );
}

export default News;
