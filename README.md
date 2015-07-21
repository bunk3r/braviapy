# braviapy
Bravia Television remote controller stuff (JSON, uPnp, DIAL, DLNA, etc), may be useful for piloting other devices too (WARNING - Still work in progress!)

Take a look at the code, feel free to modify/reuse functions.

```
$ ./bravia.py -h
Usage: ./bravia.py (-h|--help) (-p|--pin <pin>) (-v|--verbose) (-d|--discover) (-w|--wol <macaddr>) (-r|--remote)

$ ./bravia.py -d
Bravia found on 192.168.1.72

$ ./bravia.py -r
[*] AccessControl
Registered!
CLIENTID=TVSideView:eb1214c4-321d-47ab-948d-9b9ebb36354e
NICKNAME=Nexus 7 (TV SideView)
[*] getRemoteControllerInfo
[p] PowerOff: AAAAAQAAAAEAAAAvAw==
[V] VolumeUp: AAAAAQAAAAEAAAASAw==
[v] VolumeDown AAAAAQAAAAEAAAATAw==
[C] ChannelUp AAAAAQAAAAEAAAAQAw==
[c] ChannelDown AAAAAQAAAAEAAAARAw==
[0] Num0: AAAAAQAAAAEAAAAJAw==
[1] Num1: AAAAAQAAAAEAAAAAAw==
[2] Num2: AAAAAQAAAAEAAAABAw==
[3] Num3: AAAAAQAAAAEAAAACAw==
[4] Num4: AAAAAQAAAAEAAAADAw==
[5] Num5: AAAAAQAAAAEAAAAEAw==
[6] Num6: AAAAAQAAAAEAAAAFAw==
[7] Num7: AAAAAQAAAAEAAAAGAw==
[8] Num8: AAAAAQAAAAEAAAAHAw==
[9] Num9: AAAAAQAAAAEAAAAIAw==
v
V
x
Remote Controller: exit!

$ ./bravia.py -v
[*] AccessControl
Registered!
CLIENTID=TVSideView:eb1214c4-321d-47ab-948d-9b9ebb36354e
NICKNAME=Nexus 7 (TV SideView)
Cookie: auth=75f7f494196e6f02b3019030c8295df1969da5552b636aa9837777d580f7bbb4; path=/sony/; max-age=1209600; expires=Tue, 04-Aug-2015 17:33:33 GMT;

[*] getPlayingContent
Program Title: Reazione a Catena
Title: Rai 1
MediaType: tv
RESULT:  [{"programTitle": "Reazione a Catena", "tripletStr": "318.1.3401", "title": "Rai 1", "durationSec": 4200, "uri": "tv:dvbt?trip=318.1.3401&srvName=Rai%201", "source": "tv:dvbt", "dispNum": "001", "startDateTime": "2015-07-21T18:50:00+0200", "programMediaType": "tv"}]


[*] getSystemInformation
[
    {
        "product": "TV",
        "macAddr": "B0:10:41:72:C6:83",
        "name": "BRAVIA",
        "language": "ita",
        "cid": "1F74D30894F5121275F41A2B8EB9337DD62C1543",
        "generation": "2.4.1",
        "region": "ITA",
        "area": "ITA",
        "model": "KDL-50W705B",
        "serial": "0101010"
    }
]

[*] getNetworkSettings
[
    [
        {
            "ipAddrV4": "192.168.1.72",
            "netif": "wlan0",
            "ipAddrV6": "",
            "netmask": "255.255.255.0",
            "dns": [
                "217.72.96.66",
                "194.183.2.129"
            ],
            "hwAddr": "B0:10:41:72:C6:83",
            "gateway": "192.168.1.254"
        },
        {
            "ipAddrV4": "192.168.179.1",
            "netif": "p2p0",
            "ipAddrV6": "",
            "netmask": "255.255.255.0",
            "dns": [
                "0.0.0.0",
                "0.0.0.0"
            ],
            "hwAddr": "B2:10:41:72:C6:83",
            "gateway": "0.0.0.0"
        }
    ]
]

[*] getMethodTypes
[
    [
        "getColorKeysLayout",
        [],
        [
            "{\"colorKeysLayout\":\"string\"}"
        ],
        "1.0"
    ],
    [
        "getCurrentTime",
        [],
        [
            "string"
        ],
        "1.0"
    ],
    [
        "getDateTimeFormat",
        [],
        [
            "{\"dateFormat\":\"string\",\"timeFormat\":\"string\"}"
        ],
        "1.0"
    ],
    [
        "getInterfaceInformation",
        [],
        [
            "{\"productCategory\":\"string\",\"productName\":\"string\",\"modelName\":\"string\",\"serverName\":\"string\",\"interfaceVersion\":\"string\"}"
        ],
        "1.0"
    ],
    [
        "getMethodTypes",
        [
            "string"
        ],
        [
            "string",
            "string*",
            "string*",
            "string"
        ],
        "1.0"
    ],
    [
        "getNetworkSettings",
        [
            "{\"netif\":\"string\"}"
        ],
        [
            "{\"netif\":\"string\",\"hwAddr\":\"string\",\"ipAddrV4\":\"string\",\"ipAddrV6\":\"string\",\"netmask\":\"string\",\"gateway\":\"string\",\"dns\":[\"string*\"]}*"
        ],
        "1.0"
    ],
    [
        "getPostalCode",
        [],
        [
            "{\"postalCode\":\"string\"}"
        ],
        "1.0"
    ],
    [
        "getPowerSavingMode",
        [],
        [
            "{\"mode\":\"string\"}"
        ],
        "1.0"
    ],
    [
        "getPowerStatus",
        [],
        [
            "{\"status\":\"string\"}"
        ],
        "1.0"
    ],
    [
        "getRemoteControllerInfo",
        [],
        [
            "{\"bundled\":\"bool\",\"type\":\"string\"}",
            "{\"name\":\"string\",\"value\":\"string\"}*"
        ],
        "1.0"
    ],
    [
        "getSystemInformation",
        [],
        [
            "{\"product\":\"string\",\"region\":\"string\",\"language\":\"string\",\"model\":\"string\",\"serial\":\"string\",\"macAddr\":\"string\",\"name\":\"string\",\"generation\":\"string\",\"area\":\"string\",\"cid\":\"string\"}"
        ],
        "1.0"
    ],
    [
        "getSystemSupportedFunction",
        [],
        [
            "{\"option\":\"string\",\"value\":\"string\"}*"
        ],
        "1.0"
    ],
    [
        "getVersions",
        [],
        [
            "string*"
        ],
        "1.0"
    ],
    [
        "getWolMode",
        [],
        [
            "{\"enabled\":\"bool\"}"
        ],
        "1.0"
    ],
    [
        "requestToNotifyDeviceStatus",
        [
            "{\"internetTVLinkage\":{\"playingInternetTV\":\"bool\",\"showingKeyControlableGui\":\"bool\"}}"
        ],
        [
            "{\"internetTVLinkage\":{\"playingInternetTV\":\"bool\",\"showingKeyControlableGui\":\"bool\"}}"
        ],
        "1.0"
    ],
    [
        "setCurrentTime",
        [
            "{\"dateTime\":\"string\",\"timeZoneOffsetMinute\":\"int\",\"dstOffsetMinute\":\"int\"}"
        ],
        [],
        "1.0"
    ],
    [
        "setLEDIndicatorStatus",
        [
            "{\"mode\":\"string\",\"status\":\"bool\"}"
        ],
        [],
        "1.0"
    ],
    [
        "setLanguage",
        [
            "{\"language\":\"string\"}"
        ],
        [],
        "1.0"
    ],
    [
        "setPostalCode",
        [
            "{\"postalCode\":\"string\"}"
        ],
        [],
        "1.0"
    ],
    [
        "setPowerSavingMode",
        [
            "{\"mode\":\"string\"}"
        ],
        [],
        "1.0"
    ],
    [
        "setPowerStatus",
        [
            "{\"status\":\"bool\"}"
        ],
        [],
        "1.0"
    ],
    [
        "setWolMode",
        [
            "{\"enabled\":\"bool\"}"
        ],
        [],
        "1.0"
    ]
]

[*] getWolMode
[
    {
        "enabled": true
    }
]

[*] DIAL - YouTube status
(['Content-Type: text/xml;charset="utf-8"\r\n', 'Content-Length: 184\r\n', 'Connection: close\r\n', 'ACCESS-CONTROL-ALLOW-ORIGIN: *\r\n', 'Date: Tue, 21 Jul 2015 17:33:45 GMT\r\n'], '<?xml version="1.0" encoding="UTF-8"?>\n<service xmlns="urn:dial-multiscreen-org:schemas:dial">\n  <name>YouTube</name>\n  <options allowStop="true"/>\n  <state>stopped</state>\n</service>\n')

[*] UPNP - SUBSCRIBE test
uuid:a591ea80-2fce-11e5-8000-fcf1527dc699

[*] UPNP - SetMute 1 test
(['Content-Length: 272\r\n', 'Content-Type: text/xml; charset="utf-8"\r\n', 'EXT: \r\n', 'Connection: close\r\n', 'Date: Tue, 21 Jul 2015 17:33:51 GMT\r\n', 'Server: Linux/2.6 UPnP/1.0 KDL-50W705B/1.7\r\n', 'X-AV-Server-Info: av=5.0; cn="Sony Corporation"; mn="BRAVIA KDL-50W705B"; mv="1.7";\r\n', 'X-AV-Physical-Unit-Info: pa="BRAVIA KDL-50W705B";\r\n'], '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetMuteResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetMuteResponse></s:Body></s:Envelope>')
(['Content-Length: 272\r\n', 'Content-Type: text/xml; charset="utf-8"\r\n', 'EXT: \r\n', 'Connection: close\r\n', 'Date: Tue, 21 Jul 2015 17:33:51 GMT\r\n', 'Server: Linux/2.6 UPnP/1.0 KDL-50W705B/1.7\r\n', 'X-AV-Server-Info: av=5.0; cn="Sony Corporation"; mn="BRAVIA KDL-50W705B"; mv="1.7";\r\n', 'X-AV-Physical-Unit-Info: pa="BRAVIA KDL-50W705B";\r\n'], '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetMuteResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetMuteResponse></s:Body></s:Envelope>')

[*] UPNP - SetMute 0 test
(['Content-Length: 272\r\n', 'Content-Type: text/xml; charset="utf-8"\r\n', 'EXT: \r\n', 'Connection: close\r\n', 'Date: Tue, 21 Jul 2015 17:33:52 GMT\r\n', 'Server: Linux/2.6 UPnP/1.0 KDL-50W705B/1.7\r\n', 'X-AV-Server-Info: av=5.0; cn="Sony Corporation"; mn="BRAVIA KDL-50W705B"; mv="1.7";\r\n', 'X-AV-Physical-Unit-Info: pa="BRAVIA KDL-50W705B";\r\n'], '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetMuteResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetMuteResponse></s:Body></s:Envelope>')
(['Content-Length: 272\r\n', 'Content-Type: text/xml; charset="utf-8"\r\n', 'EXT: \r\n', 'Connection: close\r\n', 'Date: Tue, 21 Jul 2015 17:33:52 GMT\r\n', 'Server: Linux/2.6 UPnP/1.0 KDL-50W705B/1.7\r\n', 'X-AV-Server-Info: av=5.0; cn="Sony Corporation"; mn="BRAVIA KDL-50W705B"; mv="1.7";\r\n', 'X-AV-Physical-Unit-Info: pa="BRAVIA KDL-50W705B";\r\n'], '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetMuteResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetMuteResponse></s:Body></s:Envelope>')

[*] UPNP - UNSUBSCRIBE test
(['Connection: close\r\n', 'Date: Tue, 21 Jul 2015 17:33:53 GMT\r\n', 'Server: Linux/2.6 UPnP/1.0 KDL-50W705B/1.7\r\n', 'X-AV-Server-Info: av=5.0; cn="Sony Corporation"; mn="BRAVIA KDL-50W705B"; mv="1.7";\r\n', 'X-AV-Physical-Unit-Info: pa="BRAVIA KDL-50W705B";\r\n'], '')

$
```

