import axios from 'axios';

// Get API URL from environment or use a fallback
// Remove trailing slash to prevent double slash in URL
const API_BASE_URL = (process.env.REACT_APP_API_URL || 'https://rag-agent-production.up.railway.app').replace(/\/$/, '');

export const queryBackend = async (query) => {
  try {
    console.log(`Connecting to backend at: ${API_BASE_URL}`);
    const response = await axios.post(`${API_BASE_URL}/api/query`, { query });

    if (response?.data?.type) {
      return response.data;
    } else {
      return {
        type: "text",
        content: "Unexpected response format from backend.",
      };
    }

  } catch (error) {
    console.error("API Error:", error);
    return {
      type: "text",
      content: `Failed to connect to backend: ${error.message || "Unknown error"}`,
    };
  }
};
