#!/bin/bash

MORNING="(0.6980392156862745, 0.7019607843137254, 0.34509803921568627)"
DAYLIGHT="(0.6745098039215687, 0.792156862745098, 0.38823529411764707)"
NIGHT="(0.5568627450980392, 0.788235294117647, 0.32941176470588235)"

echo "RGB:"
shinyhunter optimize-variance "$MORNING" "$DAYLIGHT" "$NIGHT"
echo "HLS:"
shinyhunter optimize-variance "$MORNING" "$DAYLIGHT" "$NIGHT" --colormodel hls          
echo "H(LS):"
shinyhunter optimize-variance "$MORNING" "$DAYLIGHT" "$NIGHT" --colormodel hls --scalar h
echo "HL(S):"
shinyhunter optimize-variance "$MORNING" "$DAYLIGHT" "$NIGHT" --colormodel hls --scalar h --scalar l

