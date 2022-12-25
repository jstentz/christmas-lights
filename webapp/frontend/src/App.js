import React, { Component } from 'react';
import axios from "axios";
import './App.css';


axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

class App extends Component{
  constructor(props) {
    super(props);
    this.state = {
      light_pattern_list: [],
      selected_light_id: null
    };
  }

  componentDidMount() {
    this.refresh_list();
    this.get_selected_light_pattern();
  }

  refresh_list = () => {
    axios
      .get("/api/options")
      .then((res) => this.setState({ light_pattern_list: res.data }))
      .catch((err) => console.log(err));
  };

  get_selected_light_pattern = () => {
    axios
      .get("/api/selections/last")
      .then((res) => this.setState({ selected_light_id: res.data.light_pattern_id }))
      .catch((err) => console.log(err));
  }

  handle_selection = (selection_id) => {
    const date = new Date();
    date.setTime(date.getTime()-date.getTimezoneOffset()*60*1000);
    const selection = {
      light_pattern_id: selection_id,
      timestamp: date.toISOString(),
    }

    axios
      .post("/api/selections/", selection)
      .then((res) => this.get_selected_light_pattern())
      .catch((err) => console.log(err));
  }


  render_choices = () => {
    console.log(this.state.selected_light_id);
    return this.state.light_pattern_list.map((choice) => 
    <li
        key={choice.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span>
          {choice.title}
        </span>
        <span>
        {choice.description}
        </span>
        <span>
        <img src={choice.image_url} style={{ width: 100, height: 100 }}alt="new" />
        </span>
        <span>
          <button
            className="btn btn-primary"
            id={choice.id}
            onClick={e => this.handle_selection(choice.id)}
          >
            Select
          </button>    
        </span>
      </li>
    );
    
  };

  render(){
    return this.render_choices();


  }

}

export default App;
