import * as React from "react";
import ActorList from "../../components/Actor";

// interface propsType {

// }

class Actors extends React.Component {
  render() {
    const actors = [...Array(10).keys()].map((i) => {
      return {
        id: i + 1,
        name: "演员" + (i + 1),
        avatar: "https://dummyimage.com/125x125/caf4fa/",
      };
    });

    const data = {
      items: actors,
      current: 1,
      total: 50,
    }

    return <ActorList actors={data} />;
  }
}

export default Actors;
