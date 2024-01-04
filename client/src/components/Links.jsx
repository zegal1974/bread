import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";


export class Director extends React.Component {
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

export class Publisher extends React.Component {
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


export class Productor extends React.Component {
  render() {
    return (
      <Link to={"/productor/" + this.props.productor.id}>
        {this.props.productor.name}
      </Link>
    );
  }
}

Productor.propTypes = {
  productor: PropTypes.object,
};

export class Series extends React.Component {
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


export class Genre extends React.Component {
  render() {
    return (
      <Link to={"/genre/" + this.props.genre.id}>
        {this.props.genre.name}
      </Link>
    );
  }
}

Genre.propTypes = {
  genre: PropTypes.object,
};

export class Genres extends React.Component {
  render() {
    return (
      this.props.genres.map((genre) => {
        return <Genre key={genre.id} genre={genre} />
      })

    );
  }
}

Genres.propTypes = {
  genres: PropTypes.array,
};

export default { Director, Publisher, Productor, Series, Genre }