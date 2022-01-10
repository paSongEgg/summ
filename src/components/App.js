import React, { useEffect } from "react";
import axios from "axios";

function App() {
  useEffect(() => {
    axios.get("/").then((res) => console.log(res));
  });

  return (
    <div className="App">
      <h1>콘솔 확인</h1>
    </div>
  );
}

export default App;
