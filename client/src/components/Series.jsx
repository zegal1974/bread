import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

export default class Series extends React.Component {
  render() {
    return (
      <Link to={"/series/" + this.props.series.id}>
        {this.props.series.name}
      </Link>
    );
  }
}

Series.propTypes = {
  series: PropTypes.object,
};
