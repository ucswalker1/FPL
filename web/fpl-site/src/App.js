import "./App.css";
import * as React from "react";
import { useTable, useSortBy, useGlobalFilter } from "react-table";

import testData from "./data/test.json";
import { GlobalFilter } from "./componenets/globalfilter";

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
        Header: "Price",
        accessor: "price",
      },
      {
        Header: "xPoints",
        accessor: "xP",
      },
    ], 
    []
  );

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow, preGlobalFilteredRows, setGlobalFilter, state } 
    = useTable({columns, data}, useGlobalFilter, useSortBy);

  return (
    <div className="App">
      <>
      <GlobalFilter 
        preGlobalFilteredRows={preGlobalFilteredRows}
        setGlobalFilter={setGlobalFilter}
        globalFilter={state.globalFilter}
      />
      <div className="container">
        <table {...getTableProps()}>
          <thead>
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                    {column.render("Header")}
                    {column.isSorted ? (column.isSortedDesc ? " ▼": " ▲") : "  "}
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
      </>
    </div>
  );
}

export default App;
