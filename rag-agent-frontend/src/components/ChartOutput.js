import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts';

const ChartOutput = ({ labels, data }) => {
  if (!labels?.length || !data?.length) {
    return <div className="alert alert-warning mt-4">⚠️ No chart data to display.</div>;
  }

  const chartData = labels.map((label, i) => ({
    name: label,
    value: data[i]
  }));

  return (
    <div className="mt-4">
      <h5>Chart Result</h5>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#007bff" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartOutput;
