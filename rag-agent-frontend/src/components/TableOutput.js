import React from 'react';

const TableOutput = ({ columns = [], rows = [] }) => {
  const hasData = Array.isArray(columns) && columns.length > 0 && Array.isArray(rows) && rows.length > 0;

  return (
    <div className="mt-4">
      <h5 className="mb-3">Table Result</h5>

      {!hasData ? (
        <div className="alert alert-info">
          No data found to display in the table.
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-bordered table-hover table-striped align-middle">
            <thead className="table-light">
              <tr>
                <th>#</th>
                {columns.map((col, idx) => (
                  <th key={idx}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, i) => (
                <tr key={i}>
                  <td><strong>{i + 1}</strong></td>
                  {row.map((cell, j) => (
                    <td key={j}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default TableOutput;
