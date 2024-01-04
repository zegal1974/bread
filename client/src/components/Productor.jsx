import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

export default class Productor extends React.Component {
  render() {
    return (
      <Link to={"/publisher/" + this.props.productor.id}>
        {this.props.productor.name}
      </Link>
    );
  }
}

Productor.propTypes = {
  productor: PropTypes.object,
};
