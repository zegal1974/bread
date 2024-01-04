import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

export default class Director extends React.Component {
  render() {
    return (
      <Link to={"/director/" + this.props.director.id}>
        {this.props.director.name}
      </Link>
    );
  }
}

Director.propTypes = {
  director: PropTypes.object,
};
