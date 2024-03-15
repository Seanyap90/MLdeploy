import React, { useState, useEffect, useContext } from 'react';
import './InverterCard.css';
import inverterIcon from '../assets/inverter.png'
import { ServerEventsContext } from '../App';

class InverterCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      firstHalfColor: '#3a4759',
      secHalfColor: '#4e5e74'
    };
  }

  componentDidUpdate(prevProps) {
    //console.log("in function 1");
    if (this.props.alert !== prevProps.alert) {
      //console.log("in function 2");
      if (this.props.alert === 'FAULT') {
        //console.log("in1");
        this.setState({
          firstHalfColor: '#ff0000',
          secHalfColor: '#ff0001'
        });
      } else if (this.props.alert === 'ATTENTION') {
        this.setState({
          firstHalfColor: '#FFA500',
          secHalfColor: '#FFA501'
        });
      } else {
        //console.log("out1");
        this.setState({
          firstHalfColor: '#3a4759',
          secHalfColor: '#4e5e74'
        });
      }
    };
  }


  render() {

    //console.log(this.props.alert);

    return (
      <div className="inverter-card">
        <div className="first-half" style={{ backgroundColor: this.state.firstHalfColor }} >
            <img src={inverterIcon} alt="Inverter Icon" /> 
            <p></p>
        </div>
        <div className="second-half" style={{ backgroundColor: this.state.secHalfColor }}>
            <p>DC power: {this.props.dc_power} </p>
            <p>AC power: {this.props.ac_power}</p>
            <p>serial number: {this.props.serial_num}</p>
            <p>Daily Yield: {this.props.daily_yield}</p>
        </div>
      </div>
    )
  }
}

export default InverterCard;