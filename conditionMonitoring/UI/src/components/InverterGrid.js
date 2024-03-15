import React from "react";
import InverterCard from "./InverterCard";
import { Row, Col } from 'react-simple-flex-grid';
import "react-simple-flex-grid/lib/main.css";

class InverterGrid extends React.Component {
    render() {
        //console.log(this.props.item);
        return (
            <div className="inverterGrid">
                {this.props.item.map((f, index) => (
                    <Col 
                        key={index}
                        xs={{ span: 10 }} sm={{ span: 8 }} md={{ span: 5 }}
                        lg={{ span: 4 }} xl={{ span: 3 }}
                    ><InverterCard
                        key={f['uniqueId']}
                        dc_power={f['dc_power']}
                        ac_power={f['ac_power']}
                        daily_yield={f['daily_yield']}
                        serial_num={f['serial_number']}
                        alert={f['alert']}
                    />
                    </Col>
                ))}
            </div>
        )
    }
}

export default InverterGrid;