
# Event Type Decoder

## Introduction

algoseek's Options Trade+Quote, Trade+NBBO Quote, and Trade Only datasets provide `EventType` column with a byte value encoding event types applicable for each event. This command-line tool can be used to decode event type codes to string values. Please refer to dataset guide for detailed description of event types.

Python 2.7 or 3.x is required to run the script.

## Command-Line Arguments

| Short | Long          | Description                                                          |
| ----- | ------------- | -------------------------------------------------------------------- |
| -et   | --event_type  | Decode event type code                                               |
| -s    | --side        | If return event side                                                 |

## Usage

### Decode event type code

Event type 100
```
$ python3 event_type_decoder.py -et 100
FQ NB
```

Event type 172
```
$ python3 event_type_decoder.py -et 172
I
```

### Decode event type code along with event side

Event type 100
```
$ python3 event_type_decoder.py -et 100 -s
FQ NB A
```

Event type 34
```
$ python3 event_type_decoder.py -et 34 -s
OI
```