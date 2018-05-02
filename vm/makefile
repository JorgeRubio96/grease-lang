vm: vm.o
	gcc -o build/vm build/vm.o

vm.o: src/vm.c
	mkdir -p build
	gcc -c -O3 -Wall -o build/vm.o src/vm.c

clean:
	rm -rf build