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
#define LITERAL  0X2000000000000000 //literal direct in memory location
#define LITINDI  0X2010000000000000 //literal indirect memory location
#define RELATIVE 0X3000000000000000
#define INT      0x0000000000000000
#define FLOAT    0x0100000000000000
#define CHAR     0x0200000000000000
#define BOOL     0x0300000000000000
#define POINTER  0x0400000000000000
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
#define GOSUB    22
#define ADDR     23 //recibe direccion relativa, regresa direccion absoluta
#define VER      24
#define PARAM    25

typedef union {
  long i;
  double f;
  bool b;
  char c;
  uint64_t a;
} grease_var_t;

/* program counter */
uint64_t pc = 0;
uint64_t sp = 0; //Se actualiza en gosub 
uint64_t fp = 0;

/* instruction fields */
uint64_t instrNum   = 0;
uint64_t reg1       = 0;
uint64_t reg2       = 0;
uint64_t reg3       = 0;

grease_var_t * mem;

/* the VM runs until this flag becomes 0 */
int running = 1;

void halt( void ) {
    running = 0;
}

/* decode a code */
grease_var_t decode( uint64_t code )
{
  switch( code & ACCESS ){
  case DIRECT:
    return mem[code & CONTENT];
  case INDIRECT:
    return decode(mem[sp - (code & CONTENT)].a);
  case RELATIVE:
    return mem[sp - (code & CONTENT)];
  case LITERAL: {
    grease_var_t res;
    uint64_t tmp = code & CONTENT;
    switch(code & TYPE){
    case INT:
      // res.i = * (int32_t *) &tmp;
      // return res;
      return mem[code & CONTENT];
    case FLOAT:
      // res.f = * (float *) &tmp;
      // return res;
      return mem[code & CONTENT];
    case CHAR:
      // res.c = * (char *) &tmp;
      // return res;
      return mem[code & CONTENT];
    case POINTER:
      // res.a = tmp;
      // return res;
      return mem[code & CONTENT];
    default:
      printf("Error! in literal");
      halt();
    }
    break;
  case LITINDI: {
    grease_var_t res;
    uint64_t tmp = code & CONTENT;
    switch(code & TYPE){
    case INT:
      // res.i = * (int32_t *) &tmp;
      // return res;
      return decode(mem[sp - tmp].a);
    case FLOAT:
      // res.f = * (float *) &tmp;
      // return res;
      return decode(mem[sp - tmp].a);
    case CHAR:
      // res.c = * (char *) &tmp;
      // return res;
      return decode(mem[sp - tmp].a);
    case POINTER:
      // res.a = tmp;
      // return res;
      return decode(mem[sp - tmp].a);
    default:
      printf("Error! in indirect literal");
      halt();
    }
    break;

  }
  default:
    printf("Error! in decode");
    halt();
  }
}

/* decode a code */
void assign(uint64_t code, grease_var_t val )
{
  switch( code & ACCESS ){
  case DIRECT:
    mem[code & CONTENT] = val;
    break;
  case INDIRECT:
    mem[mem[code & CONTENT].a & CONTENT] = val;
    break;
  case RELATIVE:
    mem[sp - (code & CONTENT)] = val;
    break;
  default:
     printf("Error! in vm assign: %lx\n", code & ACCESS);
     halt();
  }
}

/* fetch the next code from the program */
void fetch()
{
  instrNum = mem[ pc++ ].a;
  reg1 = mem[ pc++ ].a;
  reg2 = mem[ pc++ ].a;
  reg3 = mem[ pc++ ].a;
}

/* Eval funcs */

void times( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.i = decode(reg1).i * decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.f = decode(reg1).i * decode(reg2).f;
      assign(reg3, res);
      break;
    case POINTER:
      res.a = decode(reg1).i * reg2;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in TIMES");
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case INT:
      res.f = decode(reg1).f * decode(reg2).i;
      assign(reg3, res);
      break;
    case FLOAT:
      res.f = decode(reg1).f * decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in TIMES");
      halt();
    }
    break;
  case POINTER:
    switch(reg2 & TYPE) {
    case INT:
      res.a = reg1 * decode(reg2).i;
      assign(reg3, res);
      break;
    case POINTER:
      res.a = reg1 * reg2;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in TIMES");
      halt();
    }
    break;
  default:
    printf("Error!! in TIMES");	
    halt();
  }
}

void divide( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.i = decode(reg1).i / decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.f = decode(reg1).i / decode(reg2).f;
      assign(reg3, res);
      break;
    case POINTER:
      res.a = decode(reg1).i / reg2;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in DIVIDE");
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case INT:
      res.f = decode(reg1).f / decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.f = decode(reg1).f / decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in DIVIDE");
      halt();
    }
    break;
  case POINTER:
    switch(reg2 & TYPE) {
    case INT:
      res.a = reg1 / decode(reg2).i; 
      assign(reg3, res);
      break;
    case POINTER:
      res.a = reg1 / reg2;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in DIVIDE");
      halt();
    }
    break;
  default:
    printf("Error!! in DIVIDE");	
    halt();
  }
}

void add( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.i = decode(reg1).i + decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.f = decode(reg1).i + decode(reg2).f;
      assign(reg3, res);
      break;
    case POINTER:
      res.a = decode(reg1).i + reg2;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in ADD2: %lx", reg2 & TYPE);
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case INT:
      res.f = decode(reg1).f + decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.f = decode(reg1).f + decode(reg2).f; 
      assign(reg3, res);
      break;
    default:
      printf("Error!! in ADD2: %lx", reg2 & TYPE);
      halt();
    }
    break;
  case POINTER:
    switch(reg2 & TYPE) {
    case INT:
      res.a = reg1 + decode(reg2).i; 
      assign(reg3, res);
      break;
    case POINTER:
      res.a = reg1 + reg2; 
      assign(reg3, res);
      break;
    default:
      printf("Error!! in ADD2: %lx", reg2 & TYPE);
      halt();
    }
    break;
  default:
    printf("Error!! in ADD1: %lx", reg1 & TYPE);
    halt();
  }
}

void reduct( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.i = decode(reg1).i - decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.f = decode(reg1).i - decode(reg2).f;
      assign(reg3, res);
      break;
    case POINTER:
      res.a = decode(reg1).i - reg2;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in MINUS");
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case INT:
      res.f = decode(reg1).f - decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.f = decode(reg1).f - decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in MINUS");
      halt();
    }
    break;
  case POINTER:
    switch(reg2 & TYPE) {
    case INT:
      res.a = reg1 - decode(reg2).i; 
      assign(reg3, res);
      break;
    case POINTER:
      res.a = reg1 - reg2;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in MINUS");
      halt();
    }
    break;
  default:
    printf("Error!! in MINUS");	
    halt();
  }
}

void equals( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).i == decode(reg2).i; 
      assign(reg3, res);
      break;
    default:
      printf("Error!! in equals2: %lx", reg2 & TYPE);
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case FLOAT:
      res.b = decode(reg1).f == decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in equals2: %lx", reg2 & TYPE);
      halt();
    }
    break;
  case CHAR:
    switch(reg2 & TYPE) {
    case CHAR:
      res.b = decode(reg1).c == decode(reg2).c;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in equals2: %lx", reg2 & TYPE);
      halt();
    }
    break;
  case BOOL:
    switch(reg2 & TYPE) {
    case BOOL:
      res.b = decode(reg1).b == decode(reg2).b;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in equals2: %lx", reg2 & TYPE);
      halt();
    }
    break;
  default:
    printf("Error!! in equals1: %lx", reg1 & TYPE);
    halt();
  }
}

void greaterThan( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).i > decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.b = decode(reg1).i > decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in gt");
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).f > decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.b = decode(reg1).f > decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in gt");
      halt();
    }
    break;
  case CHAR:
    switch(reg2 & TYPE) {
    case CHAR:
      res.b = decode(reg1).c > decode(reg2).c;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in gt");
      halt();
    }
    break;
  default:
    printf("Error!! in gt");
    halt();
  }
}

void greaterEqual( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).i >= decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.b = decode(reg1).i >= decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in ge");
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).f >= decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.b = decode(reg1).f >= decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in ge");
      halt();
    }
    break;
  case CHAR:
    switch(reg2 & TYPE) {
    case CHAR:
      res.b = decode(reg1).c >= decode(reg2).c;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in ge");
      halt();
    }
    break;
  default:
    printf("Error!! in ge");
    halt();
  }
}

void lessEqual( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).i <= decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.b = decode(reg1).i <= decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in le");
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).f <= decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.b = decode(reg1).f <= decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in le");
      halt();
    }
    break;
  case CHAR:
    switch(reg2 & TYPE) {
    case CHAR:
      res.b = decode(reg1).c <= decode(reg2).c;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in le");
      halt();
    }
    break;
  default:
    printf("Error!! in le");
    halt();
  }
}

void lessThan( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).i < decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.b = decode(reg1).i < decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in lt");
      halt();
    }
    break;
  case FLOAT:
    switch(reg2 & TYPE) {
    case INT:
      res.b = decode(reg1).f < decode(reg2).i; 
      assign(reg3, res);
      break;
    case FLOAT:
      res.b = decode(reg1).f < decode(reg2).f;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in lt");
      halt();
    }
    break;
  case CHAR:
    switch(reg2 & TYPE) {
    case CHAR:
      res.b = decode(reg1).c < decode(reg2).c;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in lt");
      halt();
    }
    break;
  default:
    printf("Error!! in lt");
    halt();
  }
}

void not( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case BOOL:
    res.b = !decode(reg1).b;
    assign(reg3, res);
    break;
  default:
    printf("Error!! in not");
    halt();
  }
}

void q_assign( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    res.i = decode(reg1).i;
    assign(reg3, res);
    break;
  case FLOAT:
    res.f = decode(reg1).f;
    assign(reg3, res);
    break;
  case CHAR:
    res.c = decode(reg1).c;
    assign(reg3, res);
    break;
  case BOOL:
    res.b = decode(reg1).b;
    assign(reg3, res);
    break;
  case POINTER:
    res.a = reg1;
    assign(reg3, res);
  default:
    printf("Error!! in assign");
    halt();
  }
}

void uMinus( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case INT:
    res.i = -decode(reg1).i;
    assign(reg3, res);
    break;
  case FLOAT:
    res.f = -decode(reg1).f;
    assign(reg3, res);
    break;
  default:
    printf("Error!! in uMinus");
    halt();
  }
}

void and( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case BOOL:
    switch(reg2 & TYPE) {
    case BOOL:
      res.b = decode(reg1).b && decode(reg2).b;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in and");
      halt();
    }
    break;
  default:
    printf("Error!! in and");
    halt();
  }
}

void or( void ) {
  grease_var_t res;
  switch(reg1 & TYPE) {
  case BOOL:
    switch(reg2 & TYPE) {
    case BOOL:
      res.b = decode(reg1).b || decode(reg2).b;
      assign(reg3, res);
      break;
    default:
      printf("Error!! in or");
      halt();
    }
    break;
  default:
    printf("Error!! in or");
    halt();
  }
}

void jmp( void ){
  pc = decode(reg3).a * 4;
}

void jmpF( void ) {
  //printf("JUMP: %d\n", decode(reg1).b);
  if (!decode(reg1).b)
  {
    jmp();
  }
}

void print_( void ){
  switch(reg1 & TYPE){
    case INT:
      printf("%ld", decode(reg1).i);
      break;
    case FLOAT:
      printf("%lf", decode(reg1).f);
      break;
    case CHAR:
      printf("%c", decode(reg1).c);
      break;
    case BOOL:
      printf("%s", decode(reg1).b ? "true" : "false");
      break;
    default:
      printf("Error!! in print, %lx", reg1 & TYPE);
      halt();
  }
}

void scan_( void ){
  grease_var_t buffer;
  //printf("Grease Input: ");
  switch(reg1 & TYPE){
    case INT:
      scanf("%ld", &buffer.i);
      assign(reg1, buffer);
      break;
    case FLOAT:
      scanf("%lf", &buffer.f);
      assign(reg1, buffer);
      break;
    case CHAR:
      scanf("%c", &buffer.c);
      assign(reg1, buffer);
      break;
    default:
      printf("Error!! in scan");
      halt();
  }
}

void return_( void ){
  assign(reg3, decode(reg1));
  pc = mem[sp - 1].a; // Location of return addr
  sp = mem[sp].a;     // Location of FramePointer
}

void era( void ){
  uint64_t fp = sp;                 // Save last sp
  sp += decode(reg1).a;
  mem[sp].a = fp;
}

void gosub( void ){
  mem[sp - 1].a = pc;       // Return addr
  pc = decode(reg1).a * 4;  // JMP to subroutine
}

void addr( void ){
  grease_var_t res;
  switch(reg1 & ACCESS) {
  case RELATIVE:
    res.a = sp - (reg1 & CONTENT);
    assign(reg3, res);
    break;
  case INDIRECT:
    res.a = mem[reg1 & CONTENT].a;
    assign(reg3, res);
    break;
  case DIRECT:
    res.a = reg1 & CONTENT;
    assign(reg3, res);
    break;
  default:
    printf("Error!! in addr: %lx\n", reg1 & ACCESS);
    halt();
  }
}

void param( void ){
  uint64_t fp = mem[sp].a;
  switch(reg1 & ACCESS) {
  case DIRECT:
    assign(reg3, decode(reg1));
    break;
  case RELATIVE:
    assign(reg3, mem[fp - (reg1 & CONTENT)]);
    break;
  case INDIRECT:
    assign(reg3, decode(reg1));
    break;
  case LITERAL:
    assign(reg3, decode(reg1));
    break;
  default:
    printf("Error!! in param: %lx\n", reg1 & ACCESS);
    halt();
  }
}

void ver( void ){
  //printf("VER: %lx >= %lx\n", decode(reg1).a, decode(reg2).a);
  if(decode(reg1).a >= decode(reg2).a) {
    printf("Error: Array out of bounds");
    halt();
  }
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
      q_assign();
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
      //printf("Returning!\n");
      return_();
      break;
    case ERA:
      era();
      break;
    case GOSUB:
      gosub();
      break;
    case ADDR:
      addr();
      break;
    case PARAM:
      param();
      break;
    case VER:
      ver();
      break;
    default:
    printf("Unknown opcode: %lx\n", instrNum);
    halt();
      // Err
  }
}

void run()
{
  while( running )
  {
    //printf("\nDEBUG: %u\n", pc / 4);
    fetch();
    //printf("DEBUG: %lx\n", instrNum);
    //printf("DEBUG: %lx\n", reg1);
    //printf("DEBUG: %lx\n", reg2);
    //printf("DEBUG: %lx\n", reg3);
    //printf("DEBUG: %lx\n", mem[sp].a);
    //printf("DEBUG: %lx\n", mem[sp-1].a);
    eval();
  }
}

int main( int argc, const char * argv[] )
{
  FILE *fileExec;
  uint64_t maxmem;
  long fileLen;
  //check for memory
  fileExec = fopen(argv[1], "r");
  fseek(fileExec,0,SEEK_END);
  fileLen = ftell(fileExec);
  rewind(fileExec);
  fread(&maxmem, 8, 1, fileExec);
  fread(&sp, 8, 1, fileExec);
  // Max memory 1GB
  if (maxmem > 1000000)
  {	
    // Err
    return -1;
  }
  mem = malloc(maxmem);
  fread(mem, fileLen-16, 1, fileExec);
  // running
  run();
  return 0;
}