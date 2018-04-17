/*
	Virtual machine for grease-lang
*/
#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "stdbool.h"

/* defines */
#define DIRECT   0x0000000000000000
#define INDIRECT 0x1000000000000000
#define LITERAL  0X2000000000000000
#define RELATIVE 0X3000000000000000
#define INT      0x0000000000000000
#define FLOAT    0x0100000000000000
#define CHAR     0x0200000000000000
#define BOOL     0x0300000000000000
#define ACCESS   0xF000000000000000
#define TYPE     0x0F00000000000000
#define CONTENT  0x00FFFFFFFFFFFFFF 

#define TIMES    1
#define DIVIDE   2
#define PLUS     3 
#define MINUS    4
#define EQ       5
#define GT       6
#define LT       7 
#define GE       8
#define LE       9 
#define NOT      10
#define ASSIGN   11
#define U_MINUS  12
#define JMP_F    13
#define JMP      14
#define AND      15
#define OR       16
#define PRINT    17
#define SCAN     18
#define HALT     19
#define RETURN 	 20
#define ERA      21
#define PARAM    22
#define GOSUB    23
#define ADDR     24 //recibe direccion relativa, regresa direccion absoluta


/* program counter */
unsigned int pc = 0;
unsigned int sp = 0; //Se actualiza en gosub 

/* instruction fields */
uint64_t program[];
uint64_t instrNum   = 0;
uint64_t reg1       = 0;
uint64_t reg2       = 0;
uint64_t reg3       = 0;
uint64_t return_reg = 0;
uint64_t * mem;

/* decode a code */
uint64_t decode( uint64_t code )
{

	switch( code & ACCESS ){
	case DIRECT:
		return mem[code & CONTENT];
	case INDIRECT:
		return mem[mem[code & CONTENT]];
	case LITERAL:
		return code & CONTENT;
	case RELATIVE:
		return mem[sp + ( code & CONTENT)];
	default:
	 	printf("Error! in decode");
	}
}

/* fetch the next code from the program */
void fetch()
{
  	instrNum = program[ pc++ ];
  	reg1 = decode(program[ pc++ ]);
  	reg2 = decode(program[ pc++ ]);
  	reg3 = decode(program[ pc++ ]);
}

/* the VM runs until this flag becomes 0 */
int running = 1;

/* Eval funcs */

void times( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs * (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs * (float) rhs);
			break;
		default:
			printf("Error!! in TIMES");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs * (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs * (float) rhs);
			break;
		default:
			printf("Error!! in TIMES");
		}
		break;
	default:
		printf("Error!! in TIMES");
	}
}

void divide( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs / (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs / (float) rhs);
			break;
		default:
			printf("Error!! in DIVIDE");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs / (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs / (float) rhs);
			break;
		default:
			printf("Error!! in DIVIDE");
		}
		break;
	default:
		printf("Error!! in DIVIDE");
	}
}

void add( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs + (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs + (float) rhs);
			break;
		default:
			printf("Error!! in ADD");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs + (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs + (float) rhs);
			break;
		default:
			printf("Error!! in ADD");
		}
		break;
	default:
		printf("Error!! in ADD");	
	}
}

void reduct( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs - (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs - (float) rhs);
			break;
		default:
			printf("Error!! in reduct");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs - (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs - (float) rhs);
			break;
		default:
			printf("Error!! in reduct");
		}
		break;
	default:
			printf("Error!! in reduct");
	}
}

void equals( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs == (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs == (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((int) lhs == (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((int) lhs == (bool) rhs);
			break;
		default:
			printf("Error!! in equals");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs == (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs == (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((float) lhs == (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((float) lhs == (bool) rhs);
			break;
		default:
			printf("Error!! in equals");
		}
		break;
	case CHAR:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((char) lhs == (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((char) lhs == (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((char) lhs == (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((char) lhs == (bool) rhs);
			break;
		default:
			printf("Error!! in equals");
		}
		break;
	case BOOL:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((bool) lhs == (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((bool) lhs == (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((bool) lhs == (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((bool) lhs == (bool) rhs);
			break;
		default:
			printf("Error!! in equals");
		}
		break;
	default:
		printf("Error!! in equals");
	}
}

void greaterThan( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs > (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs > (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((int) lhs > (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((int) lhs > (bool) rhs);
			break;
		default:
			printf("Error!! in gt");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs > (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs > (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((float) lhs > (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((float) lhs > (bool) rhs);
			break;
		default:
			printf("Error!! in gt");
		}
		break;
	case CHAR:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((char) lhs > (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((char) lhs > (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((char) lhs > (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((char) lhs > (bool) rhs);
			break;
		default:
			printf("Error!! in gt");
		}
		break;
	case BOOL:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((bool) lhs > (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((bool) lhs > (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((bool) lhs > (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((bool) lhs > (bool) rhs);
			break;
		default:
			printf("Error!! in gt");
		}
		break;
	default:
		printf("Error!! in gt");
	}
}

void greaterEqual( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs >= (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs >= (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((int) lhs >= (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((int) lhs >= (bool) rhs);
			break;
		default:
			printf("Error!! in ge");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs >= (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs >= (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((float) lhs >= (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((float) lhs >= (bool) rhs);
			break;
		default:
			printf("Error!! in ge");
		}
		break;
	case CHAR:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((char) lhs >= (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((char) lhs >= (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((char) lhs >= (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((char) lhs >= (bool) rhs);
			break;
		default:
			printf("Error!! in ge");
		}
		break;
	case BOOL:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((bool) lhs >= (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((bool) lhs >= (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((bool) lhs >= (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((bool) lhs >= (bool) rhs);
			break;
		default:
			printf("Error!! in ge");
		}
		break;
	default:
		printf("Error!! in ge");
	}
}

void lessEqual( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs <= (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs <= (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((int) lhs <= (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((int) lhs <= (bool) rhs);
			break;
		default:
			printf("Error!! in le");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs <= (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs <= (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((float) lhs <= (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((float) lhs <= (bool) rhs);
			break;
		default:
			printf("Error!! in le");
		}
		break;
	case CHAR:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((char) lhs <= (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((char) lhs <= (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((char) lhs <= (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((char) lhs <= (bool) rhs);
			break;
		default:
			printf("Error!! in le");
		}
		break;
	case BOOL:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((bool) lhs <= (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((bool) lhs <= (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((bool) lhs <= (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((bool) lhs <= (bool) rhs);
			break;
		default:
			printf("Error!! in le");
		}
		break;
	default:
		printf("Error!! in le");
	}
}

void not( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		mem[reg3] = (uint64_t) ((int) !lhs);
		break;
	case FLOAT:
		mem[reg3] = (uint64_t) ((float) !lhs);
		break;
	case CHAR:
		mem[reg3] = (uint64_t) ((char) !lhs);
		break;
	case BOOL:
		mem[reg3] = (uint64_t)((bool) !lhs);
		break;
	default:
		printf("Error!! in not");
	}
}

void assign( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		mem[reg3] = (uint64_t) ((int) lhs);
		break;
	case FLOAT:
		mem[reg3] = (uint64_t) ((float) lhs);
		break;
	case CHAR:
		mem[reg3] = (uint64_t) ((char) lhs);
		break;
	case BOOL:
		mem[reg3] = (uint64_t)((bool) lhs);
		break;
	default:
		printf("Error!! in assign");
	}
}

void uMinus( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		mem[reg3] = (uint64_t) ((int) -lhs);
		break;
	case FLOAT:
		mem[reg3] = (uint64_t) ((float) -lhs);
		break;
	case CHAR:
		mem[reg3] = (uint64_t) ((char) -lhs);
		break;
	case BOOL:
		mem[reg3] = (uint64_t)((bool) -lhs);
		break;
	default:
		printf("Error!! in uMinus");
	}
}

void and( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs && (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs && (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((int) lhs && (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((int) lhs && (bool) rhs);
			break;
		default:
			printf("Error!! in and");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs && (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs && (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((float) lhs && (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((float) lhs && (bool) rhs);
			break;
		default:
			printf("Error!! in and");
		}
		break;
	case CHAR:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((char) lhs && (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((char) lhs && (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((char) lhs && (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((char) lhs && (bool) rhs);
			break;
		default:
			printf("Error!! in and");
		}
		break;
	case BOOL:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((bool) lhs && (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((bool) lhs && (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((bool) lhs && (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((bool) lhs && (bool) rhs);
			break;
		default:
			printf("Error!! in and");
		}
		break;
	default:
		printf("Error!! in and");
	}
}

void or( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((int) lhs || (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((int) lhs || (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((int) lhs || (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((int) lhs || (bool) rhs);
			break;
		default:
			printf("Error!! in or");
		}
		break;
	case FLOAT:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((float) lhs || (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((float) lhs || (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((float) lhs || (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((float) lhs || (bool) rhs);
			break;
		default:
			printf("Error!! in or");
		}
		break;
	case CHAR:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((char) lhs || (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((char) lhs || (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((char) lhs || (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((char) lhs || (bool) rhs);
			break;
		default:
			printf("Error!! in or");
		}
		break;
	case BOOL:
		switch(reg2 & TYPE) {
		case INT:
			mem[reg3] = (uint64_t) ((bool) lhs || (int) rhs);
			break;
		case FLOAT:
			mem[reg3] = (uint64_t) ((bool) lhs || (float) rhs);
			break;
		case CHAR:
			mem[reg3] = (uint64_t) ((bool) lhs || (char) rhs);
			break;
		case BOOL:
			mem[reg3] = (uint64_t) ((bool) lhs || (bool) rhs);
			break;
		default:
			printf("Error!! in or");
		}
		break;
	default:
		printf("Error!! in or");
	}
}

void jmpF( void ) {
	uint64_t lhs = (reg1 & CONTENT);
	if (!lhs)
	{
		pc = (reg3 & CONTENT);	
	}
}

void jmp( void ){
	pc = (reg3 & CONTENT);
}

void halt( void ) {
	printf("VM: halt\n");
 	running = 0;
}

void print_( void ){
	uint64_t lhs = (reg1 & CONTENT);
	printf("Grease Output:\n");
	switch(reg1 & TYPE){
		case INT:
			printf("%d\n", ((int) (lhs)) );
			break;
		case FLOAT:
			printf("%f\n", ((float) (lhs)) );
			break;
		case CHAR:
			printf("%c\n", ((char) (lhs)) );
			break;
		case BOOL:
			printf("%s\n", ((bool) (lhs)) ? "true" : "false");
			break;
		default:
			printf("Error!! in print");
	}
}

void scan_( void ){
	uint64_t lhs = (reg1 & CONTENT);
	switch(reg1 & TYPE){
		case INT:
			scanf("%d\n", (int *) &lhs);
			mem[sp] = lhs; 
			break;
		case FLOAT:
			scanf("%f\n", (float *) &lhs);
			mem[sp] = lhs;
			break;
		case CHAR:
			scanf("%c\n", (char *) &lhs);
			mem[sp] = lhs;
			break;
		case BOOL:
			scanf("%d\n", (int *) &lhs);
			mem[sp] = lhs;
			break;
		default:
			printf("Error!! in scan");
	}
	
}

void return_( void ){
	uint64_t lhs = (reg1 & CONTENT);
	switch(reg1 & TYPE) {
	case INT:
		mem[return_reg] = ((int) lhs);
		break;
	case FLOAT:
		mem[return_reg] = ((float) lhs);
		break;
	case CHAR:
		mem[return_reg] = ((char) lhs);
		break;
	case BOOL:
		mem[return_reg] = ((bool) lhs);
		break;
	default:
			printf("Error!! in return");
	}

  pc = mem[sp - 2]; // Location of return addr
  sp = mem[sp - 1];     // Location of FramePointer
}

void era( void ){
	uint64_t lhs = (reg1 & CONTENT);
 	uint64_t fp = sp;                 // Save last sp
  	sp += lhs;
  	mem[sp - 1] = fp;
}

void param( void ) {
	uint64_t lhs = (reg1 & CONTENT);

	switch(reg1 & TYPE) {
	case INT:
		mem[reg3] = (uint64_t) ((int) lhs);
		break;
	case FLOAT:
		mem[reg3] = (uint64_t) ((float) lhs);
		break;
	case CHAR:
		mem[reg3] = (uint64_t) ((char) lhs);
		break;
	case BOOL:
		mem[reg3] = (uint64_t)((bool) lhs);
		break;
	default:
			printf("Error!! in param");
	}
}

void gosub( void ){
  mem[sp - 2] = pc + 1;      // Return addr
	pc = (reg1 & CONTENT);     // JMP to subroutine
}
	

/* evaluate the last decoded instruction */
void eval()
{
  switch( instrNum )
  {
  	case TIMES:
      times();
      break;
    case DIVIDE:
      divide();
      break;
    case PLUS:
      add();
      break;
    case MINUS:
      reduct();
      break;
    case EQ:
      equals();
      break;
    case GT:
      greaterThan();
      break;
    case LT:
      lessThan();
      break;
    case GE:
      greaterEqual();
      break;
    case LE:
      lessEqual();
      break;
    case NOT:
      not();
      break;
    case ASSIGN:
      assign();
      break;
    case U_MINUS:
      uMinus();
      break;
    case JMP_F:
      jmpF();
      break;
    case JMP:
      jmp();
      break;
    case AND:
      and();
      break;
    case OR:
      or();
      break;
    case PRINT:
      print_();
      break;
    case SCAN:
      scan_();
      break;
    case HALT:
      halt();
      break;
    case RETURN:
      return_();
      break;
    case ERA:
      era();
      break;
    case PARAM:
      param();
      break;
    case GOSUB:
      gosub();
      break;
    default:
    	// Err
  }
}

/* display all registers as 4-digit hexadecimal words */
void showRegs()
{
  int i;
  printf( "regs = " );
  for( i=0; i<NUM_REGS; i++ )
    printf( "%04X ", regs[ i ] );
  printf( "\n" );
}

void run()
{
  while( running )
  {
    showRegs();
    fetch();
    eval();
  }
  showRegs();
}

int main( int argc, const char * argv[] )
{
	FILE *fileExec;
	uint64_t maxmem;
	long fileLen;
	//check for memory
	fileExec = fopen(argv[1]);
	fseek(fileExec,0,SEEK_END);
	fileLen = ftell(fileExec);
	rewind(fileExec);
	fread(&maxmem, 4, 1, fileExec);
	//get memory 1GB
	if (maxmem > 1000000)
	{	
		// Err
		return -1;
	}

	mem = malloc(maxmem);
  return_reg = fileLen-3;
	fread(mem, fileLen-4, 1, fileExec);
	// running
	run();
	return 0;
}
