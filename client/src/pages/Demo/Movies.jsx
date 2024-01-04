import * as React from "react";
import { MovieList } from "../../components/Movie";

// interface propsType {

// }

class Movies extends React.Component {
  render() {
    const movies = [...Array(5).keys()].map((i) => {
      return {
        id: i,
        name: "影片名字" + i,
        thumb: "https://dummyimage.com/147x200/caf4fa/",
        code: "ABC-001",
        published_on: "2023-12-01",
      };
    });

    return <MovieList movies={movies} />;
  }
}

export default Movies;
