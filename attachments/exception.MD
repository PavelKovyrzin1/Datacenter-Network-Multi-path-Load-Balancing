| Exception                      | Description                                               |
|--------------------------------|-----------------------------------------------------------|
| `INVALID_NODE_LINK`            | two nodes have no link, but you send through it           |    
| `EXCEED_BAND_WIDTH_OUT`        | messages which switch send is more than its bandwidth-out | 
| `SEND_MESSAGE_TWICE`           | single message is send twice at one time-segment          |
| `INVALID_MESSAGE`              | send a message which is not in this switch right now      |
| `CHANGE_TARGET`                | message's target_node_id info is changed invalidly        | 
| `INVALID_TARGET_SERVER`        | message is send to none-target server                     |
| `INVALID_SWITCH_STATS_INFO`    | SwitchStatsInfo.info meet with wrong data-range           | 
| `MESSAGE_TYPE_ERROR`           | Message has wrong type                                    | 
| `SWITCH_STATS_INFO_TYPE_ERROR` | SwitchStatsInfo has wrong type                            | 
| `INVALID_ADD_ATTRIBUTES`       | message or statsInfo is added with invalid attribute      | 
