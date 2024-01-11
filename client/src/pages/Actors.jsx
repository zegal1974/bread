import React, { useState, useEffect } from 'react';
import ActorList from "../components/Actor";
import Loading from "../components/Loading";
import { useQuery } from 'react-query';  

// interface propsType {

// }

class Actors extends React.Component {

  const { data, loading, error } = userQuery("users", getActers, {
    variables: { page: 1, pageSize: 10}
  });

  render() {
    if loading return <Loading />
    if error return <Error />
    return <ActorList actors={data} />
  }
}

export default Actors;
