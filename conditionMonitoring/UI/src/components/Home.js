import React, { useState, useEffect, useContext } from 'react';
import './Home.css'
import DcacInvert from "../data/inverterData";
import InverterGrid from './InverterGrid';
import { Row, Col } from 'react-simple-flex-grid';
import "react-simple-flex-grid/lib/main.css";
import { ServerEventsContext } from '../App';

function Home(){
    const [gridData, setGridData] = useState([
        { label: 'Current Time', value: 'Loading...' },
        { label: 'Current Alerts', value: 'Loading...' },
        { label: 'Irradiation', value: 'Loading...' },
        { label: 'Solar Panel Temp', value: 'Loading...' },
    ]);
    const [allInverter, setAllInverter] = useState(DcacInvert);
    const [numAlerts, setNumAlerts] = useState('0')
    const [numAttn, setNumAttn] = useState('0')

    const items = [{item: DcacInvert}]

    const serverData = useContext(ServerEventsContext);
    // if (serverData) {
    //     if (Object.keys(serverData).length > 2) {
    //         console.log("second in:" + serverData.SENSOR_NUM);
    //     } else {
    //         console.log("alert from:"+ serverData.inverter_id);
    //     }
    // }
    

    useEffect(() => {
        if (serverData) {
            if (Object.keys(serverData).length > 2) {
                console.log("third in:" + serverData.SENSOR_NUM);
                const updateInvItem = () => {
                    const invItem = DcacInvert.find((item) => item.uniqueId === parseInt(serverData.SENSOR_NUM));
                    if (invItem) {
                        //console.log(invItem);
                        var updates = [
                            {parameter: 'dc_power', newValue: serverData.DC_POWER},
                            {parameter: 'ac_power', newValue: serverData.AC_POWER},
                            {parameter: 'daily_yield', newValue: serverData.DAILY_YIELD},
                            {parameter: 'serial_number', newValue: serverData.SOURCE_KEY}
                        ]
                
                        const updatedInvItem = {...invItem};
                        updates.forEach((update) => {
                            updatedInvItem[update.parameter] = update.newValue;
                        });
        
                        const updatedAllInvItems = allInverter.map((item) => {
                            if (item.uniqueId === parseInt(serverData.SENSOR_NUM)) {
                                return updatedInvItem;
                            }
                            return item;
                        });
        
                        setAllInverter(updatedAllInvItems)
                    }
                };
        
                updateInvItem();  

            } else {
                //console.log(serverData);
                console.log("alert is: " + serverData.alert)
                const updateInvAlert = () => {
                    const invItem = allInverter.find((item) => item.uniqueId === parseInt(serverData.inverter_id));
                    if (invItem) {
                        var updates = [
                            {parameter: 'alert', newValue: serverData.alert}
                        ]

                        const updatedInvItem = {...invItem};
                        updates.forEach((update) => {
                            updatedInvItem[update.parameter] = update.newValue;
                        });

                        const updatedAllInvItems = allInverter.map((item) => {
                            if (item.uniqueId === parseInt(serverData.inverter_id)) {
                                return updatedInvItem;
                            }
                            return item;
                        });
        
                        setAllInverter(updatedAllInvItems)
                    }
                };

                updateInvAlert();
                //console.log('inverters:' + allInverter);

                const countStatus = (status) => {
                    return allInverter.filter(inverter => inverter.alert === status).length;
                }

                //console.log(countStatus);

                // Count number of Fault statuses
                const faultCount = countStatus('FAULT'); 
                setNumAlerts(faultCount);   

                const attnCount = countStatus('ATTENTION');
                setNumAttn(attnCount);
            }   
        }
        
    }, [serverData])

    useEffect(() => {
        if (serverData) {
            //console.log(Object.keys(serverData).length);
            if (Object.keys(serverData).length > 2) {
                const { DATE_TIME, IRRADIATION, MODULE_TEMPERATURE } = serverData;
                setGridData([
                    { label: 'Current Time', value: DATE_TIME || 'N/A' },
                    { label: 'Current Alerts', value: `Faults: ${numAlerts},  Attn: ${numAttn}`},
                    { label: 'Irradiation', value: IRRADIATION || 'N/A' },
                    { label: 'Solar Panel Temp', value: MODULE_TEMPERATURE || 'N/A' },
                ]);
            }            
        }
    }, [serverData]);

    return(
        <main className="main-container">
            <div className="first-section">
                <h1>Solar Power Generation Check</h1>
                <div className="grid">
                    {gridData.map((data, index) => (
                        <div key={index} className="grid-box">
                            <h3>{data.label}</h3>
                            <p>{data.value}</p>
                        </div>
                    ))}
                </div>
            </div>
            <div className="second-section">
                <h1>Inverter Monitoring</h1>
                <InverterGrid item={allInverter} />
            </div>

        </main>
    );
}

export default Home;
