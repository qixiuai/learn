import React, { Component } from 'react';
import {
  Alert,
  AppRegistry,
  Button,
  Image,
  Text,
  TextInput,
  ScrollView,
  StyleSheet,
  View,
} from 'react-native';


class Blink extends Component {
  constructor(props) {
    super(props);
    this.state = { isShowingText: true };
    setInterval( () => (
      this.setState(previousState => (
	{ isShowingText: !previousState.isShowingText }
      ))
    ), 1000);
  }

  render() {
    if (!this.state.isShowingText) {
//      return null;
    }
    return (
	<Text style={styles.bigblue}>{ this.props.text }</Text>
    );
  }
  
}

class Header extends Component {
  render() {
    return (
	<Text style={this.props.style}> {this.props.text} </Text>
    )
  }
}

class Task extends Component {
  constructor(props) {
    super(props);
    this.state = {text: ""};
  }
  render() {
    return (
	<View style={{padding: 10}}>
	<Text style={{padding: 10, fontSize: 42}}>
	  {this.state.text.split(' ').map((word) => word && word).join(' ')}
        </Text>	
	<TextInput
          style={{height: 100, fontSize: 20}}
          placeholder="type your task"
          onChangeText={ (text) => this.setState({text})}
	/>
	<Button onPress={() => {Alert.alert(this.state.text)}} title="Submit"/>	
      </View>
    )
  }
}

class TaskList extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
	<ScrollView>
	<Task style={this.props.style} />
	<Task style={this.props.style} />
	<Task style={this.props.style} />
	</ScrollView>
    )
  }
}

class Player extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <Text> </Text>
    )
  }
}


export default class App extends Component {
  render() {
    return (
	<View style={styles.container}>
	<Header style={styles.header} text="BrainMaster" />
	<TaskList style={styles.red} />
        <Text style={styles.bigblue}> Hello World! </Text>
	<Blink text="blink blink" />
	</View>
    );
  }
}

const styles = StyleSheet.create({
    container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'space-evenly',
  },
  header: {
    color: 'green',
    fontWeight: 'bold',
    fontSize: 50,
  },

  bigblue: {
    color: 'blue',
    fontWeight: 'bold',
    fontSize: 30,
  },
  red: {
    color: 'green',
    fontSize: 30,
//    fontWeight: 'bold',
  }
});


AppRegistry.registerComponent("DeepBrain", () => App);
