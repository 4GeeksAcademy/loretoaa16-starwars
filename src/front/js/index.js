//import react into the bundle
import React from "react";
import ReactDOM from "react-dom/client";

//include your index.scss file into the bundle
import "../styles/index.css";

//import your own components
import Layout from "./Layout.jsx";

//render your react application
const root = ReactDOM.createRoot(document.getElementById("app"));
root.render(<Layout/>);
