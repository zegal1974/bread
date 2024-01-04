import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

export default class Publisher extends React.Component {
  render() {
    return (
      <Link to={"/publisher/" + this.props.publisher.id}>
        {this.props.publisher.name}
      </Link>
    );
  }
}

Publisher.propTypes = {
  publisher: PropTypes.object,
};
