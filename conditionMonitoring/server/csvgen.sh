#!/bin/bash

# Function to send data to server and handle response
send_data_to_server() {
    local response
    tail -n +2 /home/pi/condition_monitoring/data1/plant_ml3.csv | while IFS=, read -r -a columns; do
        local json_data="{"
        for ((i = 0; i < ${#columns[@]}; ++i)); do
            # Trim leading and trailing spaces from field value
            value=$(echo "${columns[i]}" | awk '{$1=$1};1')
            # Extract header (first row of CSV file)
            header=$(head -n 1 /home/pi/condition_monitoring/data1/plant1_ml.csv | cut -d ',' -f$((i + 1)) | awk '{$1=$1};1' | sed 's/ /_/g')
            json_data+="\"$header\":\"$value\""
            if [ $i -lt $((${#columns[@]} - 1)) ]; then
                json_data+=","
            fi
        done
        json_data+="}"
        response=$(curl -s -X POST -H "Content-Type: application/json" --data "$json_data" http://localhost:8080/sendData)
        echo "Received server response: $response"
        sleep 1.5
    done
}

send_data_to_server
