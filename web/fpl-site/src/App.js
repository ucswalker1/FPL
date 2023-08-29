import "./App.css";
import * as React from "react";
import { useTable } from "react-table";

import testData from "./data/test.json";

function App() {
  const data = React.useMemo(() => testData, [])
  const columns = React.useMemo(() => [
      {
        Header: "Player",
        accessor: "name",
      },
      {
        Header: "Position",
        accessor: "pos",
      },
      {
        Header: "Team",
        accessor: "team",
      },
      {
        Header: "xPoints",
        accessor: "xP",
      },
    ], 
    []
  );

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({columns, data});

  return (
    <div className="App">
      <div className="container">
        <table {...getTableProps()}>
          <thead>
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <th {...column.getHeaderProps()}>
                    {column.render("Header")}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row) => {
              prepareRow(row)
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map((cell) => (
                    <td {...cell.getCellProps()}>
                       {cell.render("Cell")}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
