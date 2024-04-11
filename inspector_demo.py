import pandas as pd

sample = pd.read_csv('realtime.csv')

tag_ddos = ''
tag_slow_rate = ''
tag_mitm = ''


if sample['SSIP'].values > 1000:
    tag_ddos = 'DDOS '
if sample['SSIP'].values > 100 and sample['SSIP'].values == sample['SFE'].values:
    tag_slow_rate = 'Slow Rate '
if sample['MISS_MAC'].values == 1:
    tag_mitm = 'MITM '
if tag_ddos == '' and tag_slow_rate == '' and tag_mitm == '':
    tag = 'Normal'
else:
    tag = tag_ddos + tag_slow_rate + tag_mitm

print(tag)
