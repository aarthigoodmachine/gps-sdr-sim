# Makefile for Linux etc.

.PHONY: all clean time
all: gps-sdr-sim

SHELL=/bin/bash
CC=gcc
CFLAGS=-O3 -Wall -D_FILE_OFFSET_BITS=64
ifdef USER_MOTION_SIZE
CFLAGS+=-DUSER_MOTION_SIZE=$(USER_MOTION_SIZE)
endif
LDFLAGS=-lm

gps-sdr-sim: gpssim.o
	${CC} $< ${LDFLAGS} -o $@

gpssim.o: .user-motion-size gpssim.h download-ephemeris

download-ephemeris: brew-install-wget
	$(eval LATEST_FILE=$(shell python3 -c "\
	from ftplib import FTP; \
	ftp = FTP('cddis.gsfc.nasa.gov'); \
	ftp.login(); \
	ftp.cwd('/gnss/data/daily/$(YEAR)/brdc'); \
	file_names = ftp.nlst(); \
latest_file = sorted(file_names)[-1]; \
print(latest_file.split('.')[0])"))
	YEAR=$(shell date +"%Y"); \
	Y=$(patsubst 20%,%,$(YEAR)); \
	LATEST=; \
	wget -q ftp://cddis.gsfc.nasa.gov/gnss/data/daily/$(YEAR)/brdc/$(LATEST).$(Y)n.Z -O $@.Z
	uncompress $@.Z

brew-install-wget:
	$(shell brew install wget)

.user-motion-size: .FORCE
	@if [ -f .user-motion-size ]; then \
		if [ "`cat .user-motion-size`" != "$(USER_MOTION_SIZE)" ]; then \
			echo "Updating .user-motion-size"; \
			echo "$(USER_MOTION_SIZE)" >| .user-motion-size; \
		fi; \
	else \
		echo "$(USER_MOTION_SIZE)" > .user-motion-size; \
	fi;

clean:
	rm -f gpssim.o gps-sdr-sim *.bin .user-motion-size

time: gps-sdr-sim
	time ./gps-sdr-sim -e brdc3540.14n -u circle.csv -b 1
	time ./gps-sdr-sim -e brdc3540.14n -u circle.csv -b 8
	time ./gps-sdr-sim -e brdc3540.14n -u circle.csv -b 16

.FORCE:
	

YEAR?=$(shell date +"%Y")
Y=$(patsubst 20%,%,$(YEAR))
%.$(Y)n:
	wget -q ftp://cddis.gsfc.nasa.gov/gnss/data/daily/$(YEAR)/brdc/$@.Z -O $@.Z
	uncompress $@.Z
