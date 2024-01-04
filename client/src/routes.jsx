// import React from "react";
// import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import BasicLayout from "./layouts/BasicLayout";

import Index from "./pages/Index";
import Demo from "./pages/Demo";
import Actors from "./pages/Demo/Actors";
import Movie from "./pages/Demo/Movie";
import Movies from "./pages/Demo/Movies";

const routes = [
  {
    path: "/",
    // exact: true,
    element: <BasicLayout />,
    title: "Home",
    children: [{ index: true, component: Index }],
  },
  {
    path: "demo",
    element: <BasicLayout />,
    // component: BasicLayout,
    title: "Demo",
    children: [
      { index: true, element: <Demo />, title: "Demo index" },
      { path: "actor/:id", element: <Movies />, title: "Movies" },
      { path: "actors", element: <Actors />, title: "Actors" },
      { path: "movie/:code", element: <Movie />, title: "Movie" },
      { path: "movies", element: <Movies />, title: "Movies" },
    ],
  },
  {
    path: "test",
    element: <BasicLayout />,
    title: "test",
  },
];

export default routes;
