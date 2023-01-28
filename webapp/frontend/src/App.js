import React, { Component } from 'react';
import axios from "axios";
import { Grid, Text} from '@nextui-org/react';
import './App.css';
import { NextUIProvider } from '@nextui-org/react';
import { GridItem } from './GridItem'
import { ErrorMessage } from './ErrorMessage'


axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

function buildHeaders(currentPath) {
  const headers = {
    headers: {
      API_AUTH: currentPath
    }
  };
  return headers;
}

const password = window.location.pathname.substring(1, window.location.pathname.length - 1);
const auth_headers = buildHeaders(password);

class App extends Component{
  constructor(props) {
    super(props);
    this.state = {
      light_pattern_list: [],
      selected_light_pattern: null,
      error_message: {
        message: "really long message I bet you don't know anything about this super long message it's like really long haha what the heck man.",
        hidden: false
      }
    };
  }   

  componentDidMount() {
    axios.all([
      axios.get("/api/options/", auth_headers),
      axios.get("/api/selections/last/", auth_headers)
    ])
    .then(axios.spread((res1, res2) => {
      const light_pattern_list = this.convert_to_dict(res1.data);
      const light_pattern_selection = res2.data.light_pattern_id;
      this.setState({light_pattern_list: light_pattern_list, selected_light_pattern: light_pattern_selection});
    }))
    .catch((err) => this.handleAxiosError(err));
  }

  convert_to_dict = (lp_list) => {
    var light_pattern_dict = {};

    for (var i = 0; i < lp_list.length; i++) {
      light_pattern_dict[ lp_list[i].id ] = lp_list[i];
    }
    return light_pattern_dict;

  };

  refresh_list = () => {
    axios
      .get("/api/options/", auth_headers)
      .then((res) => this.setState({ light_pattern_list: this.convert_to_dict(res.data)}))
      .catch((err) => this.handleAxiosError(err));
  };

  get_selected_light_pattern = () => {
    axios
      .get("/api/selections/last/", auth_headers)
      .then((res) => this.setState({ selected_light_pattern: res.data.light_pattern_id }))
      .catch((err) => this.handleAxiosError(err));
  }

  handle_selection = (selection_id, selection_name) => {
    const date = new Date();
    date.setTime(date.getTime()-date.getTimezoneOffset()*60*1000);
    const selection = {
      light_pattern_id: selection_id,
      timestamp: date.toISOString(),
    }

    axios
      .post("/api/selections/", selection, auth_headers)
      .then((res) => this.get_selected_light_pattern())
      .catch((err) => this.handleAxiosError(err));

    axios
      .post("/api/selections/updatepi/", {"light_pattern_id": selection_id, "light_pattern_name": selection_name}, auth_headers)
      .catch((err) => this.handleAxiosError(err));
  }

  handle_reset_parameters = (selection_id, selection_name) => {
    axios
    .post("/api/options/reset_parameters/", {"light_pattern_id": selection_id, "light_pattern_name": selection_name}, auth_headers)
    .then((this.refresh_list()))
    .catch((err) => console.log(err));
  }

  handle_edit_parameters = (selection_id, selection_name, new_params) => {
    axios
    .post("/api/options/update_parameters/", {"light_pattern_id": selection_id, "light_pattern_name": selection_name, "parameters": new_params}, auth_headers)
    .catch((err) => this.handleAxiosError(err));
  }

  handleAxiosError(err) {
    console.log(err);
    this.setState({error_message: {
      message: err.response.data,
      hidden: false
    }});
  }

  handle_error_message_close = () => {
    this.setState({error_message: {message: "", hidden: true}});
  }

  render_choices = () => {
    var selection_text, selection_description;
    if(this.state.selected_light_pattern === null || this.state.light_pattern_list === null || this.state.light_pattern_list.length === 0) {
      selection_text = "None! Select one below.";
      selection_description = "None! Select one below.";
    } else {
      selection_text = this.state.light_pattern_list[this.state.selected_light_pattern].title;
      selection_description = this.state.light_pattern_list[this.state.selected_light_pattern].description;
    }
    const light_pattern_list = Object.values(this.state.light_pattern_list);

    return (
      <NextUIProvider>
        <ErrorMessage 
          message={this.state.error_message.message} 
          hide={this.state.error_message.hidden} 
          errorMessageCloseCallback={this.handle_error_message_close} 
        />
        <Text h1
        css={{
          textGradient: "45deg, $red600 35%, $green600 65%",
          textAlign: "center",        }}
        weight="bold">Plaid Family Holiday Lights</Text>
        <Text h3 color="#2A2B2A" css={{textAlign: "center"}}>Select a light pattern. Watch the tree change. Enjoy!</Text>
        <Text h4 color="#706C61" css={{textAlign:"center"}}>Current Selection: {selection_text}</Text>
        <Text color="#706C61" css={{textAlign:"center"}}>{selection_description}</Text>
        <div className="outer-container">
        <Grid.Container gap={2} className="grid-container">
          {light_pattern_list.map((choice) => 
          <GridItem 
            selectionCallback={this.handle_selection}
            resetParametersCallback={this.handle_reset_parameters}
            editParametersCallback={this.handle_edit_parameters}
            params={choice.parameters_json} 
            name={choice.title} 
            image_url={choice.image_url} 
            key={choice.id} 
            light_id={choice.id} 
            light_name={choice.animation_id}/>
          )}
        </Grid.Container>
        </div>
      </NextUIProvider>

    );
 
  };
  render(){
    return this.render_choices();
  }

}

export default App;
