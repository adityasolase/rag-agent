import axios from 'axios';

const API_BASE_URL = window._env_?.API_URL || process.env.REACT_APP_API_URL;

export const queryBackend = async (query) => {
  try {
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
