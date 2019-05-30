#!/usr/bin/env python

import operator
import re
import sys

path = sys.argv[1]

total_requests = 0
total_data = 0
resource_counts = {}
host_counts = {}
status_counts = {}
pattern = re.compile('^([^\s]+)\s([^\s]+)\s([^\s]+)\s\[([^\]]+)\]\s"([^\s]+)\s([^\s]+)\s([^"]+)"\s([0-9]+)\s([^\s]+).*')
with open(path, 'r') as handle:
	for line in handle:
		matches = re.match(pattern, line)
		try:
			remotehost = matches.group(1)
			resource = matches.group(6)
			status = int(matches.group(8))
			try:
				bytes = int(matches.group(9))
			except:
				bytes = 0
		except Exception as e:
			continue

		total_requests += 1
		total_data += bytes

		if(resource not in resource_counts): resource_counts[resource] = 0
		resource_counts[resource] += 1
			
		if(remotehost not in host_counts): host_counts[remotehost] = 0
		host_counts[remotehost] += 1

		status_group = status / 100
		if(status_group not in status_counts): status_counts[status_group] = 0
		status_counts[status_group] += 1

print('Total Requests: {0}'.format(total_requests))
print('Total Data transmitted: {0}GiB'.format(float(total_data) / 2**30))

sorted_resources = sorted(
	resource_counts.items(),
	key=operator.itemgetter(1),
	reverse=True)
sorted_hosts = sorted(
	host_counts.items(),
	key=operator.itemgetter(1),
	reverse=True)

print('Most requested resource: {0}'.format(sorted_resources[0][0]))
print('Total requests for {0}: {1}'.format(
	sorted_resources[0][0],
	sorted_resources[0][1]))
print('Percentage of requests for {0}: {1}'.format(
	sorted_resources[0][0],
	100 * sorted_resources[0][1] / float(total_requests)))
print('Remote host with the most requests: {0}'.format(sorted_hosts[0][0]))
print('Total requests from {0}: {1}'.format(
	sorted_hosts[0][0],
	sorted_hosts[0][1]))
print('Percentage of requests from {0}: {1}'.format(
	sorted_hosts[0][0],
	100 * sorted_hosts[0][1] / float(total_requests)))
for status, count in sorted(status_counts.items()):
	print('Percentage of {0}xx requests: {1}'.format(
		status,
		100 * count / float(total_requests)))
