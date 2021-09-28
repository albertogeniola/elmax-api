from enum import Enum


class AlarmArmStatus(Enum):
    ARMED_TOTALLY = "Totale"
    ARMED_P1 = "P1"
    ARMED_P2 = "P2"
    ARMED_P1_P2 = "P1+P2"
    NOT_ARMED = "DIS"


class AlarmStatus(Enum):
    TRIGGERED = "in Allarme"
    ARMED_STANDBY = "Inserita e a riposo"
    NOT_ARMED_TRIGGERED = "non inserita e zone aperte"
    NOT_ARMED_NOT_TRIGGERED = "non inserita e pronta all'inserimento"
    NOT_ARMED_NOT_ARMABLE = "non inserita e non pronta all'inserimento"
