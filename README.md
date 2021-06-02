# Tanium ATT&CK mapping

Read our blog to see how easy it is to make an ATT&CK mapping of the detection capabilities that are available in Tanium Threat Response:

https://www.siriussecurity.nl/blog/2021/6/2/mapping-vendor-products-to-mitre-attack-tanium

**TLDR:**

Tanium offers functionality to create detections, called signals, in their Threat Response module. Those signals provide realtime monitoring on endpoint telemetry events. Besides the possibility to create your own signals, Tanium offers a feed of signals. This is a regularly updated set of signals that are designed to detect common attack behaviour. And, YES those signals are already mapped to ATT&CK! So within the feed that Tanium provides (which is a JSON file) and within their GUI you can find the ATT&CK technique ID’s for each signal. Well that’s great… but we want more! We want to have an ATT&CK Navigator overview with the detection coverage of the Tanium signals-feed. And when we have that, we want to compare it with our own use cases / detections, other products and threat actor behaviour.

# Getting started

- Download the latest version of the [Tanium signals feed](https://content.tanium.com/files/misc/ThreatResponse/ThreatResponse.html). Choose the V3 version.
- Clone the [DeTT&CT project](https://github.com/rabobank-cdc/DeTTECT) and install it [locally](https://github.com/rabobank-cdc/DeTTECT/wiki/Installation-and-requirements#local-installation). Or run the available [Docker container](https://github.com/rabobank-cdc/DeTTECT/wiki/Installation-and-requirements#docker).
- Clone this repository and install: `pip install -r requirements.txt`

# Create ATT&CK Navigator layer for Tanium
The Python script in this repository walks through the JSON file from the Tanium signals feed and creates a DeTT&CT techniques administration YAML file. With the help of DeTT&CT we are able to create an ATT&CK Navigator layer file from that YAML file.

First, let’s create a YAML file from the Tanium signals feed with the Python script:

`python tanium_attack_mapping.py -f signals_v3.21.0.0000.json`

The output of this command is a new DeTT&CT techniques administration YAML file which we need in the next step. Within the YAML file the signal names are listed within the location field of the detection object for the relevant technique. The platform (Windows, Linux, Mac) mentioned within each signal is reflected in the applicable_to field of the detection object.

Next we can easily create an ATT&CK Navigator file by using DeTT&CT with the following command:

`python dettect.py d -ft techniques-tanium.yaml -l`

The result is our JSON file that can be loaded into the (ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/).

Within DeTT&CT you can have scores up to 5 which will reflect how good the detections are in your environment. The scores used in this layer file are all set to "1", because we would like to encourage you to go over the signals yourself.