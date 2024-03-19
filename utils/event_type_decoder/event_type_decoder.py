#!/usr/bin/python3

import argparse


# 7th bit signalling buy side
BUYSIDE_FLAG = -128
NBBO_FLAG = 64
# 1 for call, 0 for put
CALL_FLAG = 32
# previous trade/quote cancelled
CANCEL_FLAG = 16
    
# type value mask (bits 0..2 used to store the field value = 0..7)
TYPE_MASK = 15
 
# type values 
Heartbeat = 0
Trade = 1
OpenInterest = 2
TradeInterest = 3
FirmQuote = 4
NonFirmQuote = 5
Rotation = 6
Halted = 7
NoQuote = 8
SessionEnd = 9
UnderlyingValueSale = 10
UnderlyingValueQuote = 11
Indicative = 12


def setup_parser():
    '''Command line arguments parser'''
    parser = argparse.ArgumentParser(description='Convert event type codes to string')
    parser.add_argument('-et', '--event_type', type=int, action='store', help='Decode event type code')
    parser.add_argument('-s', '--side', default=False, action='store_true', help='If return event side')
    
    return parser
 
def opra_event_type_to_action():
    '''Convert event type code to string'''
    event_type = args.event_type
    et = event_type & TYPE_MASK
    act = ""
    
    if et == Trade:
        if event_type & CANCEL_FLAG:
            act += "C"
        else:
            act += "T"
        if event_type & NBBO_FLAG:
            act += " NB"
    elif et == OpenInterest:
        act += "OI"
    elif et == TradeInterest:
        act += "TI"
    elif et == FirmQuote:
        act += "FQ"
        if event_type & NBBO_FLAG:
            act += " NB"
    elif et == NonFirmQuote:
        act += "NFQ"
        if event_type & NBBO_FLAG:
            act += " NB"
    elif et == Rotation:
        act += "R"
        if event_type & NBBO_FLAG:
            act += " NB"
    elif et == Halted:
        act += "H"
    elif et == NoQuote:
        act += "NQ"
        if event_type & NBBO_FLAG:
            act += " NB"
    elif et == UnderlyingValueSale:
        act += "US"
    elif et == UnderlyingValueQuote:
        act += "UQ"
    elif et == Indicative:
        act += "I"
    else:
        # INVALID
        act += "IN"
    
    return act

def event_side():
    '''Get event side'''
    et = args.event_type
    
    if et & BUYSIDE_FLAG:
        return 'B'
    else:
        return 'A'


parser = setup_parser()
args = parser.parse_args()

act = opra_event_type_to_action()

if args.side:
    if act not in ('OI', 'T', 'IN'):
        side = event_side()
        print(f"{act} {side}")
    else:
        print(f"{act}")
else:
    print(f"{act}")