# Multi-Label-Attacks-Detection

## Run controller

```bash
python3.8 pox.py forwarding.l2_learning_new
```

## Run Mininet

```bash
sudo python3.8 custom_intervlan.py
```

## Collect data

```bash
source collect.sh
```

## Run detect Mismatch MitM

```bash
python3.8 detect_mismatch.py
```

# Run attacks

## Run MitM attack from H2 to H1 and H9

### Check MAC address before attack

```bash
ettercap -T -i h2-eth0 -M ARP /10.10.0.1// /10.20.0.9//
```

## Run MitM mitigation

```bash
python3.8 Tracking_Flow_Entries.py
```

## Run Slow Rate attack from H5 to H11

```bash
python3.8 attack.py -i h5 -d 10.20.0.11
```

## Run DDoS and Slow Rate mitigation

```bash
python3.8 mitigation_dos.py
```

## Run DDoS attack from H3 to H10

```bash
sudo hping3 -S --faster -V -p 80 10.20.0.10 --rand-source
```
