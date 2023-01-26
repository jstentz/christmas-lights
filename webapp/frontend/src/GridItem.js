import React, { Component } from 'react';
import { Grid } from '@nextui-org/react';
import Icon from './cog-white.png';

export class GridItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      editing: false,
      cardClickAnimation: false,
      parameters: this.props.params
    };

    // See https://reactjs.org/docs/handling-events.html
    this.handleEditButtonClick = this.handleEditButtonClick.bind(this);
    this.handleCancelButtonClick = this.handleCancelButtonClick.bind(this);
    this.handleResetButtonClick = this.handleResetButtonClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleParameterEdit = this.handleParameterEdit.bind(this);
    this.handleCardClicked = this.handleCardClicked.bind(this);
  }

  handleEditButtonClick(e) {
    e.stopPropagation();
    this.setState({editing: true});
  }

  handleCancelButtonClick(e) {
    this.setState({editing: false});
  }

  handleResetButtonClick(e) {
    e.preventDefault();
    this.props.resetParametersCallback(this.props.light_id, this.props.light_name);
  }

  handleChange(parameter_key, e) {
    this.setState(function(oldState) {
      return {parameters: {...oldState.parameters, [parameter_key]: e.target.value}}
    });
  }

  handleParameterEdit(e) {
    e.preventDefault();
    this.setState({editing: false});
    this.props.editParametersCallback(this.props.light_id, this.props.light_name, this.state.parameters);
  }

  handleCardClicked(e) {
    e.stopPropagation();
    this.setState({cardClickAnimation: true})
    this.props.selectionCallback(this.props.light_id, this.props.light_name);
  }

  render() {
    const cardClassName = this.state.cardClickAnimation ? "card run-click-animation" : "card";

    const displayCard = (
      <Grid xs={12} sm={4} md={3} lg={2}>
        <div className={cardClassName} onClick={this.handleCardClicked} onAnimationEnd={() => this.setState({cardClickAnimation: false})}>
          <img className="card-background" src={this.props.image_url} alt={this.props.light_name} />
          <img src={Icon} className="edit-button" onClick={this.handleEditButtonClick} alt="edit" />
          <div className="container">
            <h4><b>{this.props.name}</b></h4>
          </div>
        </div>
      </Grid>
    );
    
    const editingCard = (
      <Grid xs={12} sm={4} md={3} lg={2}>
        <div className="edit-card">
          <form onSubmit={this.handleParameterEdit}>
            <p>Edit parameters for {this.props.light_name}</p>
            <div className="parameter-grid">
                {Object.entries(this.props.params).map(([key, value]) => {
                  return (
                    <React.Fragment key={key}>
                      <label htmlFor={key}>{key}</label>
                      <div className='input-container'>
                        <input type="text" name={key} value={this.state.parameters[key]} onChange={(e) => this.handleChange(key, e)} />
                      </div>
                    </React.Fragment>
                  );
                })}
            </div>
            <button type="submit">Save</button>
            <button onClick={this.handleCancelButtonClick}>Cancel</button>
            <button onClick={this.handleResetButtonClick}>Reset</button>
          </form>
        </div>
      </Grid>
    );

    return this.state.editing ? editingCard : displayCard;
  }
}