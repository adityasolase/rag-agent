import React, { useState } from 'react';
import { queryBackend } from './api';
import TextOutput from './components/TextOutput';
import TableOutput from './components/TableOutput';
import ChartOutput from './components/ChartOutput';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);

    try {
      const result = await queryBackend(query);

      
      if (result?.type === "text" || result?.type === "chart" || result?.type === "table") {
        setResponse(result);
      } else {
        setResponse({
          type: "text",
          content: "Unknown response type received from backend.",
        });
      }

    } catch (error) {
      console.error("Error during request:", error);
      setResponse({
        type: "text",
        content: "Something went wrong. Please try again.",
      });
    }

    setLoading(false);
  };

  const renderResponse = () => {
    if (!response) return null;

    switch (response.type) {
      case 'text':
        return <TextOutput text={response.content} />;

      case 'table':
        return (
          <TableOutput
            columns={response.columns || []}
            rows={response.rows || []}
          />
        );

      case 'chart':
        return (
          <ChartOutput
            labels={response.labels || []}
            data={response.data || []}
          />
        );

      default:
        return (
          <div className="alert alert-warning mt-3">
            Unsupported response type: <strong>{response.type}</strong>
            <pre>{JSON.stringify(response, null, 2)}</pre>
          </div>
        );
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Natural Language Wealth Query Agent</h2>

      <form onSubmit={handleSubmit}>
        <div className="input-group mb-3">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            type="text"
            className="form-control"
            placeholder="Ask a question like 'Top 5 portfolios' or 'Breakup by manager'..."
            required
          />
          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      </form>

      {loading && <div className="text-center mt-3">Loading response...</div>}

      {!loading && renderResponse()}
    </div>
  );
}

export default App;
