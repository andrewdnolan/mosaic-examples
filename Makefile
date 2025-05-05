N ?= 10

render: figs/SOwISC12to30E3r3_SST.pdf \
	figs/IcoswISC30E3r5_NH_si-concentration.pdf \
	figs/mpas.gis4to40km_with_IcoswISC30E3r5.pdf

profile:
	@./profile.sh $(N) ./src/ocean.py
	@./profile.sh $(N) ./src/seaice.py
	@./profile.sh $(N) ./src/landice.py

figs/SOwISC12to30E3r3_SST.pdf : ./src/ocean.py
	@python3 $?

figs/IcoswISC30E3r5_NH_si-concentration.pdf : ./src/seaice.py
	@python3 $?

figs/mpas.gis4to40km_with_IcoswISC30E3r5.pdf : ./src/landice.py
	@python3 $?

clean:
	rm -r figs/*.pdf
