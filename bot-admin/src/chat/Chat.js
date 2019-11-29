import React, { Component } from 'react'
import constants from "../constants";
import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import {Grid, Row} from "react-flexbox-grid";

export default class Chat extends Component {
  state = {
    messages: [],
    reconnects: 0,
  };
  ws = new WebSocket(constants.WEBSOCKET_URL);
  maxReconnects = 5;

  get reconnectTimeout() {
    return 1000 * Math.pow(2, this.state.reconnects);
  }

  reassignHandlersFor(ws) {
    this.setState(state => ({reconnects: state.reconnects + 1}));
    ws.onopen = () => {
      // on connecting, do nothing but log it to the console
      console.log('connected');
      this.setState(state => ({reconnects: 0}));
    };

    ws.onmessage = evt => {
      // on receiving a message, add it to the list of messages
      const message = {text: evt.data, author: 'Bot'};
      this.addMessage(message);
    };
    ws.onclose = () => {
      if (this.state.reconnects > this.maxReconnects) {
          console.log('Stop reconnecting.');
          this.setState(state => ({reconnects: 0}));
          return;
      }
      console.log(
          `Disconnected. Reconnect in ${this.reconnectTimeout / 1000}s`
      );
      // automatically try to reconnect on connection loss
      setTimeout(() => {
        this.ws = new WebSocket(constants.WEBSOCKET_URL);
        this.reassignHandlersFor(this.ws);
      }, this.reconnectTimeout);
    }
  }

  componentDidMount() {
    this.reassignHandlersFor(this.ws);
  }
  componentDidUpdate(prevProps, prevState, snapshot) {
    this.messagesEnd.scrollIntoView({ behavior: "smooth" });
  }
  addMessage = message => {
    this.setState(state => ({ messages: [message, ...state.messages] }));
  };

  submitMessage = messageString => {
    // on submitting the ChatInput form, send the message, add it to the list and reset the input
    this.ws.send(messageString);
    this.addMessage({ author: 'You', text: messageString });
  };

  render() {
    return (
      <Grid fluid>
        <Row style={{"flexDirection": "column", "height": "99vh"}}>
          <div style={{flex: 1, overflow: "auto"}}>
            {[...this.state.messages].reverse().map((message, index) =>
              <ChatMessage
                key={index}
                position={index}
                message={message.text}
                name={message.author}
                onResendButtonPressed={this.submitMessage}
              />
            )}
            <div ref={(el) => { this.messagesEnd = el; }}></div>
          </div>
          <div style={{flex: 1, "maxHeight": "40px"}}>
            <ChatInput
              onSubmitMessage={messageString => this.submitMessage(messageString)}
            />
          </div>
        </Row>
      </Grid>
    );
  }
}
