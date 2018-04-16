/*
	Virtual machine for grease-lang
*/
#import "stdio.h"
#import "stdlib.h"
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

/* fetch the next code from the program */
void fetch()
{
  	instrNum = program[ pc++ ];
  	reg1 = decode(program[ pc++ ]);
  	reg2 = decode(program[ pc++ ]);
  	reg3 = decode(program[ pc++ ]);
}

/* instruction fields */
uint64_t instrNum = 0;
uint64_t reg1     = 0;
uint64_t reg2     = 0;
uint64_t reg3     = 0;
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
	 	// Err
	}
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
			// Err
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
			// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
			// Err
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
			// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
			// Err
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
			// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
			// Err
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
			// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
		// Err
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
		// Err
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
		// Err
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
			// Err
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
			// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
			// Err
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
			// Err
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
			// Err
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
			// Err
		}
		break;
	default:
		// Err
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
	uint64_t rhs = (reg2 & CONTENT);
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
			// Err
	}
}

void scan_( void ){
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
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
			// Err
	}
	scanf("%" SCNu64 "\n", &lhs);
}

void return_( void ){
	uint64_t lhs = (reg1 & CONTENT);
	uint64_t rhs = (reg2 & CONTENT);
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
		// Err
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

void param( void )
{
	uint64_t lhs = (reg1 & CONTENT);
	switch(reg1 & TYPE){
		case INT:
			break;
		case FLOAT:
			break;
		case CHAR:
			break;
		case BOOL:
			break;
		default:
			// Err
	}
}

void gosub( void )
{
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
	fread(mem, fileLen-4, 1, fileExec);
	// running
	run();
	return 0;
}
