import React, { Component } from 'react';

export class ErrorMessage extends Component {

  render() {
    return (
      <div className="error-message" hidden={this.props.hide}>
        <button className="btn-close" onClick={this.props.errorMessageCloseCallback}>
          <span className='cross'></span>
        </button>
        <p>{this.props.message}</p>
      </div>
    )
  }
}