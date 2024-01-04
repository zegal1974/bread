import "../Base.css";
import "./Actor.css";

import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Flex, Pagination } from "antd";

class ActorCard extends React.Component {
  render() {
    return (
      <Link
        className="avatar-box text-center"
        to={"actor/" + this.props.actor.id}
      >
        <div className="photo-frame">
          <img src={this.props.actor.avatar} title={this.props.actor.name} />
        </div>
        <div className="photo-info">
          <span>{this.props.actor.name}</span>
        </div>
      </Link>
    );
  }
}

ActorCard.propTypes = {
  actor: PropTypes.object,
  // {
  //   name: PropTypes.string.isRequired,
  //   avatar: PropTypes.string.isRequired
  // }
};

class ActorInfo extends React.Component {
  render() {
    return (
      <Link
        className="avatar-box text-center"
        to={"actor/" + this.props.actor.id}
      >
        <div className="photo-frame">
          <img src={this.props.actor.avatar} title={this.props.actor.name} />
        </div>
        <div className="photo-info">
          <span>{this.props.actor.name}</span>
        </div>
      </Link>
    );
  }
}

ActorInfo.propTypes = {
  actor: PropTypes.object,
};

class ActorList extends React.Component {
  render() {
    console.log(this.props);
    const actors = this.props.actors.items.map((actor) => {
      return (
        <div className="item" key={actor.id}>
          <ActorCard actor={actor} />
        </div>
      );
    });

    return (
      <>
        <Flex>
          <div className="waterfall">{actors}</div>
        </Flex>
        <Flex>
          <Pagination
            defaultCurrent={this.props.actors.current}
            total={this.props.actors.total}
          />
        </Flex>
      </>
    );
  }
}

ActorList.propTypes = {
  actors: PropTypes.object,
};

export default ActorList;
