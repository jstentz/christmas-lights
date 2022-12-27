import React, { Component } from 'react';
import axios from "axios";
import { Grid, Card, Text, Col} from '@nextui-org/react';
import './App.css';
import { NextUIProvider } from '@nextui-org/react';


axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const GridItem = ({callbackfn, text, imageurl, lightid }) => {
  return (
   <Card isHoverable isPressable 
   onPress={() => callbackfn(lightid)}>
     <Card.Body css={{ p: 0 }}>
     <Card.Image
       src={imageurl}
       objectFit="cover"
       width="100%"
       height={350}
       alt="Card image background"
      /> 
      <Card.Footer isBlurred
      css={{
        position: "absolute",
        bgBlur: "#0f111466",
        bottom: 0,
        zIndex: 1,
      }}>
       <Col>
         {/* <Text size={14} weight="bold" transform="uppercase" color="#ffffffaa">
           Select This Light Pattern
         </Text> */}
         <Text h4 color="white">
           {text}
         </Text>
       </Col>
     </Card.Footer>
 </Card.Body>
   </Card>
 );}

class App extends Component{
  constructor(props) {
    super(props);
    this.state = {
      light_pattern_list: [],
      selected_light_pattern: null
    };
  }   

  componentDidMount() {
    this.refresh_list();
    this.get_selected_light_pattern();
  }

  shouldComponentUpdate(newProps, newState) {
    // only render if the state has changed
    return this.state.selected_light_pattern !== newState.selected_light_pattern;
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
      .get("/api/options")
      .then((res) => this.setState({ light_pattern_list: this.convert_to_dict(res.data)}))
      .catch((err) => console.log(err));


    
  };

  get_selected_light_pattern = () => {
    axios
      .get("/api/selections/last")
      .then((res) => this.setState({ selected_light_pattern: res.data.light_pattern_id }))
      .catch((err) => console.log(err));
  }

  handle_selection = (selection_id) => {
    const date = new Date();
    date.setTime(date.getTime()-date.getTimezoneOffset()*60*1000);
    const selection = {
      light_pattern_id: selection_id,
      timestamp: date.toISOString(),
    }
    console.log(selection);

    axios
      .post("/api/selections/", selection)
      .then((res) => this.get_selected_light_pattern())
      .catch((err) => console.log(err));

    axios
      .post("/api/selections/updatepi/", {"light_pattern_id": selection_id})
      .catch((err) => console.log(err));
  }



  render_choices = () => {
    // const selection_text = this.state.selected_light_pattern == null? "None! Select one below." : this.state.light_pattern_list[this.state.selected_light_pattern].title;
    // const selection_description =  this.state.selected_light_pattern == null? "None! Select one below." : this.state.light_pattern_list[this.state.selected_light_pattern].description;
    // const light_pattern_list = Object.values(this.state.light_pattern_list);
    const urls = ["https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",
                  "https://www.helpguide.org/wp-content/uploads/king-charles-spaniel-resting-head.jpg",];
    return (
      // <NextUIProvider>
      //   <Text h1
      //   css={{
      //     textGradient: "45deg, $red600 35%, $green600 65%",
      //     textAlign: "center",        }}
      //   weight="bold">Plaid Family Holiday Lights</Text>
      //   <Text h3 color="#2A2B2A" css={{textAlign: "center"}}>Select a light pattern. Watch the tree change. Enjoy!</Text>
      //   <Text h4 color="#706C61" css={{textAlign:"center"}}>Current Selection: {selection_text}</Text>
      //   <Text color="#706C61" css={{textAlign:"center"}}>{selection_description}</Text>
      //   <div className="outer-container">
      //   <Grid.Container gap={2} justify="flex-start">
      //     {light_pattern_list.map((choice) => 
      //     <Grid xs={12} sm={4} md={3} lg={2} key={choice.id}>
      //       <GridItem callbackfn={this.handle_selection} text={choice.title} imageurl={choice.image_url} lightid={choice.id}/>
      //     </Grid>
      //     )}
      //   </Grid.Container>
      //   </div>
      // </NextUIProvider>
      <NextUIProvider>
        <Grid.Container gap={2}>
          {urls.map((img_src) => 
            <Grid xs={12} sm={4} md={3} lg={2}>
              <img src={img_src}></img>
            </Grid>
          )}
      </Grid.Container>
      </NextUIProvider>

    );
 
  };
  render(){
    return this.render_choices();
  }

}

export default App;
