import React, {Component} from 'react'

export default class ChatMessage extends Component {
    render() {
        return (
            <p>
                <strong>[{this.props.position}]</strong><strong>{this.props.name}</strong> <em>{this.props.message}</em>
                <button onClick={this.handleResend}>resend</button>
            </p>

        )
    }
    handleResend = () => {
        if (this.props.onResendButtonPressed) {
            this.props.onResendButtonPressed(this.props.message)
        }
    }
}