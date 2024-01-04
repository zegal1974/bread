import "../Base.css";
import "./Movie.css";

import React from "react";
import PropTypes from "prop-types";
import { Director, Publisher, Productor, Series, Genres } from "./Links";
import { Link } from "react-router-dom";
import { Image } from "antd";

class MovieCard extends React.Component {
  render() {
    return (
      <Link
        className="movie-box text-center"
        to={"/demo/movie/" + this.props.movie.code}
      >
        <div className="photo-frame">
          <img src={this.props.movie.thumb} title={this.props.movie.name} />
        </div>
        <div className="photo-info">
          <span>{this.props.movie.name}</span>
          <br></br>
          <small>{this.props.movie.code}</small>&nbsp;/&nbsp;
          <small>{this.props.movie.published_on}</small>
        </div>
      </Link>
    );
  }
}

MovieCard.propTypes = {
  movie: PropTypes.object,
  // {
  //   name: PropTypes.string.isRequired,
  //   avatar: PropTypes.string.isRequired
  // }
};

export class MovieList extends React.Component {
  render() {
    // console.log(this.props);
    let acs = this.props.movies.map((movie) => {
      return (
        <div className="item" key={movie.id}>
          <MovieCard movie={movie} />
        </div>
      );
    });

    return (
      <div className="row">
        <div className="waterfall">{acs}</div>
      </div>
    );
  }
}

MovieList.propTypes = {
  movies: PropTypes.array,
};

export class MovieDetails extends React.Component {
  render() {
    return (
      <div className="row movie">
        <div className="col-md-9 screencap">
          <a className="bigImage" href={this.props.movie.cover}>
            <Image src={this.props.movie.cover} title={this.props.movie.name} />
          </a>
        </div>
        <div className="col-md-3 info">
          <p>
            <span className="header">识别码:</span>
            <span style={{ color: "#CC0000" }}>{this.props.movie.code}</span>
          </p>
          <p>
            <span className="header">发行日期:</span>
            {this.props.movie.published_on}
          </p>
          <p>
            <span className="header">长度:</span>
            {this.props.movie.length}分钟
          </p>
          <p>
            <span className="header">导演:</span>
            <Director director={this.props.movie.director} />
          </p>
          <p>
            <span className="header">发行商:</span>
            <Publisher publisher={this.props.movie.publisher} />
          </p>
          <p>
            <span className="header">制片商:</span>
            <Productor productor={this.props.movie.productor} />
          </p>
          <p>
            <span className="header">系列:</span>
            <Series series={this.props.movie.series} />
          </p>
          <p className="header">
            <span className="header">类别:</span>
            <Genres genres={this.props.movie.genres} />
          </p>
        </div>
      </div>
    );
  }
}

MovieDetails.propTypes = {
  movie: PropTypes.object,
};

export default { MovieList, MovieDetails };
