import time

from datetime import datetime
from equipment.transformer import Transformer
from equipment.breaker import Breaker
from equipment.capacitor_bank import CapacitorBank
from database.database import create_tables, insert_telemetry, get_telemetry
from database.database import (
    create_tables,
    insert_telemetry,
    get_telemetry,
    get_asset_telemetry,
    get_average_metric,
    get_max_metric,
    get_latest_metric,
    get_latest_readings,
    insert_health_reports,
    get_health_reports,
    insert_event
)
from database.database import get_events

from health_monitor import evaluate_transformer_health

def display_operator_dashboard(

    transformer_data,
    breaker_data,
    capacitor_data,
    dashboard_health,
    active_alarms,
    event_history
):
    
    print()
    print("=" * 50)
    print(" SUBSTATION OPERATOR DASHBOARD")
    print("=" * 50)

    normal_count = 0
    warning_count = 0
    critical_count = 0

    for health in dashboard_health.values():

        if health["status"] == "NORMAL":
            normal_count += 1

        elif health["status"] == "WARNING":
            warning_count += 1

        elif health["status"] == "CRITICAL":
                    critical_count += 1

    if critical_count > 0:
        system_status = "CRITICAL"

    elif warning_count > 0:
        system_status = "WARNING"

    else: 
        system_status = "NORMAL"

    print()
    print(f"SYSTEM STATUS: {system_status}")

    print()
    print(f"NORMAL: {normal_count}")
    print(f"WARNNG: {warning_count}")
    print(f"CRITICAL: {critical_count}")

    print()
    print("ACTIVE ALARMS")
    print("-" * 50)

    for asset_id, alarm in active_alarms.items():

        print(
            f"{asset_id} | "
            f"{alarm['status']} |"
            f"{alarm['reason']}"
        )

    print()
    print("EVENT HISTORY")
    print("-" * 50)

    for event in event_history[-10:]:
        
        print(
            f"{event['timestamp']} | "
            f"{event['asset_id']} | "
            f"{event['event_type']} | "
            f"{event['details']} | "

        )





    print()
    print("TRANSFORMERS")
    print("-" * 50)

    for transformer in transformer_data:

        asset_id = transformer["asset_id"]

        health = dashboard_health.get(asset_id)

        print(
            f"{asset_id} | "
            f"Temp: {transformer['temperature']} F | "
            f"Load: {transformer['load_percent']}% | "
            f"Voltage: {transformer['voltage']} V | "
            f"Status: {health['status']}"
        )
    print()
    print("BREAKERS")
    print("-" * 50)

    for breaker in breaker_data:
        print(
            f"{breaker['asset_id']} | "
            f"Status: {breaker['status']} | "
            f"Current: {breaker['current']} A"
        )
    print()
    print("CAPACITOR BANKS")
    print("-" * 50)

    for capacitor in capacitor_data:
        print(
            f"{capacitor['asset_id']} | "
            f"Status: {capacitor['status']} | "
            f"Reactive Power: {capacitor['reactive_power']} kvar"
        )



def display_health_report( 
        asset_id,
        average_voltage,
        max_temperature,
        latest_load,
        health_status,
        health_score,
        health_reason,
        temps
):
    print(f"==== {asset_id} Health Report ====")
    print(f"Average Voltage: {average_voltage:.2f} V")
    print(f"Maximum Temperature: {max_temperature:.2f} F")
    print(f"Current Load: {latest_load:.2f} %")

    print()
    print(f"Health Status: {health_status}")
    print(f"Health Score: {health_score:.2f}")
    print(f"Reason: {health_reason}")

    print()
    print("Latest Temperatures:")
    print(temps    )



def run_monitoring_cycle(): 
    #update equipment
    for transformer in transformers:
        transformer.update()

    for transformer in transformers:
        asset_id = transformer.asset_id
        previous_mode = previous_modes.get(asset_id)
        current_mode = transformer.simulation_mode

        if previous_mode != current_mode:
            print(
                f"MODE CHANGE: "
                f"{asset_id} | "
                f"{previous_mode} -> {current_mode}"
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            event_history.append({
                "timestamp": timestamp,
                "asset_id": asset_id,
                "event_type": "MODE CHANGE",
                "details": f"{previous_mode} -> {current_mode}"
            })

            previous_modes[asset_id] = current_mode

    for breaker in breakers:
        breaker.update()

    for capacitor in capacitors:    
        capacitor.update()

    # Telemetry collection
    transformer_data = []
    
    for transformer in transformers:
        transformer_data.append(
            transformer.get_telemetry()
        )

    breaker_data = []

    for breaker in breakers:
        breaker_data.append(
            breaker.get_telemetry()
        )


    capacitor_data = []

    for capacitor in capacitors:
            capacitor_data.append(
                capacitor.get_telemetry()
            )
# Stores transformer telemetry
    for data in transformer_data:

        insert_telemetry(
            data["asset_id"],
            "voltage",
            data["voltage"],
            str(data["timestamp"])
        )

        insert_telemetry(
            data["asset_id"],
            "current",
            data["current"],
            str(data["timestamp"])
        )

        insert_telemetry(
            data["asset_id"],
            "temperature",
            data["temperature"],
            str(data["timestamp"])
        )

        insert_telemetry(
            data["asset_id"],
            "load_percent",
            data["load_percent"],
            str(data["timestamp"])
        )
    for data in breaker_data:
        insert_telemetry(
                data["asset_id"],
                "current",
                data["current"],
                str(data["timestamp"])
                )
    for data in capacitor_data:
        insert_telemetry(
                data["asset_id"],
                "reactive power",
                data["reactive_power"],
                str(data["timestamp"])
                )

    return transformer_data, breaker_data, capacitor_data


def analyze_transformer_health(
        asset_id, 
        transformer_data,
        previous_status
):

    average_voltage = get_average_metric(
        asset_id,
        "voltage"
    )

    max_temperature = get_max_metric(
        asset_id,
        "temperature"
    )

    latest_load = get_latest_metric(
        asset_id,
        "load_percent"
    )  


    temps = get_latest_readings(
        asset_id,
        "temperature",
        5
    )

    temps = temps[::-1]

    increasing = 0

    if len(temps) >= 5:

        for i in range(len(temps) - 1):

            if temps[i][0] < temps[i+1][0]:
                increasing += 1

    health_status, health_reason, health_score = evaluate_transformer_health(
        transformer_data["temperature"],
        latest_load,
        average_voltage,
        increasing
    )

    if health_status != previous_status:

        insert_event(
            asset_id,
            previous_status,
            health_status,
            health_reason,
            str(transformer_data["timestamp"])
        )

    insert_health_reports(
        transformer_data["asset_id"],
        health_status,
        health_score,
        health_reason,
        str(transformer_data["timestamp"])
    )

    return (
        average_voltage,
        max_temperature,
        latest_load,
        health_status,
        health_reason,
        health_score,
        temps
    )

    
create_tables()


# create equipment
transformers = [
    Transformer("TX-101"),
    Transformer("TX-102"),
    Transformer("TX-103")
    ]

transformers[0].simulation_mode = "NORMAL"
transformers[1].simulation_mode = "OVERLOAD"
transformers[2].simulation_mode = "NORMAL"


breakers = [
    Breaker("BR-101"),
    Breaker("BR-102"),
    Breaker("BR-103")
    ]
capacitors = [
    CapacitorBank("CB-101"),
    CapacitorBank("CB-102"),
    CapacitorBank("CB-103")
    ]

# Set equipment status
breakers[0].status = "CLOSED"
capacitors[0].status = "ON"

previous_health_status = {
    transformer.asset_id: "NORMAL"
    for transformer in transformers
}

previous_modes = {
    transformer.asset_id: transformer.simulation_mode
    for transformer in transformers
}


active_alarms = {}

event_history = []

simulation_mode = "NORMAL"

while True:

    transformer_data, breaker_data, capacitor_data = run_monitoring_cycle()

    dashboard_health = {}


    print("===== TRANSFORMERS =====")

    for data in transformer_data:
        print(data)

    print()

    print("===== BREAKERS =====")

    for data in breaker_data:
        print(data)

    print()

    print("===== CAPACITORS =====")

    for data in capacitor_data:
        print(data)

    print()

    for data in transformer_data:

        asset_id = data["asset_id"]

        previous_status = previous_health_status.get(
            asset_id,
            "NORMAL"
        )

        (
            average_voltage,
            max_temperature,
            latest_load,
            health_status,
            health_reason,
            health_score,
            temps
        ) = analyze_transformer_health(

            asset_id,
            data,
            previous_status

        )

        previous_health_status[asset_id] = health_status

        dashboard_health[asset_id] = {

            "status": health_status,
            "score": health_score,
            "reason": health_reason
        }

        if health_status != "NORMAL":

            if asset_id not in active_alarms:

                active_alarms[asset_id] = {

                    "status": health_status,
                    "reason": health_reason
                }

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                event_history.append({

                    "timestamp": timestamp,
                    "asset_id": asset_id,
                    "event_type": "NEW ALARM",
                    "details": health_status
                })

                print()
                print(f"NEW ALARM: {asset_id}")

        if health_status == "NORMAL":

            if asset_id in active_alarms:

                del active_alarms[asset_id]

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                
                event_history.append({

                    "timestamp": timestamp,
                    "asset_id": asset_id,
                    "event_type": "ALARM CLEARED",
                    "details": "NORMAL"
                })

                print()
                print(f"ALARM CLEARED: {asset_id}")

        display_health_report(
            asset_id,
            average_voltage,
            max_temperature,
            latest_load,
            health_status,
            health_score,
            health_reason,
            temps
        )

    display_operator_dashboard(
            transformer_data,
            breaker_data,
            capacitor_data,
            dashboard_health,
            active_alarms,
            event_history
    )

    events = get_events()

    print()
    print("===== EVENT HISTORY =====")

    for event in events:
        print(event)

    time.sleep(2)



