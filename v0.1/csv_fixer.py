#!/usr/bin/env python3

f = open("test.csv", "r")
for x in f:
	v = x.replace("\n", "").split(",")
	print(str(v[0])+","+str(v[1])+","+str(v[2])+","+str(int(v[3])/1000))


