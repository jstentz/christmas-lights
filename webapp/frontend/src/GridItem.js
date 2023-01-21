import React, { Component } from 'react';
import { Grid } from '@nextui-org/react';
import Icon from './cog-white.png';

export class GridItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      editing: false,
      cardClickAnimation: false
    };

    // See https://reactjs.org/docs/handling-events.html
    this.handleEditButtonClick = this.handleEditButtonClick.bind(this);
    this.handleCancelButtonClick = this.handleCancelButtonClick.bind(this);
    this.handleCardClicked = this.handleCardClicked.bind(this);
  }

  handleEditButtonClick(e) {
    e.stopPropagation();
    this.setState({editing: true});
  }

  handleCancelButtonClick(e) {
    e.stopPropagation();
    this.setState({editing: false});
  }

  handleCardClicked(e) {
    e.stopPropagation();
    this.setState({cardClickAnimation: true})
    //setTimeout(() => this.setState({cardClickAnimation: false}), 1100);

    this.props.callbackfn(this.props.light_id, this.props.light_name);
  }

  render() {
    console.log(this.props.params);
    const cardClassName = this.state.cardClickAnimation ? "card run-click-animation" : "card";
    const displayCard = (
      <Grid xs={12} sm={4} md={3} lg={2} className="four-by-three-aspect">
        <div className={cardClassName} onClick={this.handleCardClicked} onAnimationEnd={() => this.setState({cardClickAnimation: false})}>
          <img className="card-background" src={this.props.image_url} alt={this.props.light_name}/>
          <img src={Icon} className="edit-button" onClick={this.handleEditButtonClick} />
          <div className="container">
            <h4><b>{this.props.name}</b></h4>
          </div>
        </div>
      </Grid>
    );
    
    const editingCard = (
      <Grid xs={12} sm={4} md={3} lg={2} className="four-by-three-aspect">
        <div className="edit-card">
          <form>
            <p>Edit parameters for {this.props.light_name}</p>
            <table>
            {Object.entries(this.props.params).map(([key, value]) => {
              return (
                  <tr key={key}>
                    <td><label>{key}</label></td>
                    <td><input type="text" name={key} value={value}></input></td>
                  </tr>
              );
            })}
            </table>
            <button type="submit">Save</button>
            <button onClick={this.handleCancelButtonClick}>Cancel</button>
            <button>Reset</button>
          </form>
        </div>
      </Grid>
    );
    return this.state.editing ? editingCard : displayCard;
  }
}