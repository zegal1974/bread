import * as React from "react";
import { MovieDetails } from "../../components/Movie";

// interface propsType {
// }

class Movie extends React.Component {
  render() {
    const movie = {
      id: "1",
      name: "影片名字",
      thumb: "https://dummyimage.com/147x200/caf4fa/",
      cover: "https://dummyimage.com/800x538/caf4fa/",
      code: "ABC-001",
      length: 100,
      published_on: "2023-12-01",
      director: { id: "1", name: "导演名字", },
      publisher: { id: '2', name: "发行商名字", },
      productor: { id: '5', name: "制片商名字", },
      series: { id: '5', name: "系列名字", },
      genres: [{ id: "1", name: "类别1" }, { id: "2", name: "类别2" }, { id: "4", name: "类别4" }]

    };

    return <MovieDetails movie={movie} />;
  }
}

export default Movie;
