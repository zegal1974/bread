import * as React from "react";
import ActorList from "../components/Actor";

// interface propsType {

// }

class Demo extends React.Component {
  render() {
    const actors = [...Array(5).keys()].map((i) => {
      return {
        id: i,
        name: "演员" + i,
        avatar: "https://dummyimage.com/125x125/caf4fa/",
      };
    });

    return <ActorList actors={actors} />;
  }
}

export default Demo;
