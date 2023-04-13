/****************************************************/
/* File: main.c                                     */
/* Main program for TINY compiler                   */
/* Compiler Construction: Principles and Practice   */
/* Kenneth C. Louden                                */
/****************************************************/
//改自原main.c文件，产生语法树
#include "globals.h"
#include "parse.h"
#include "util.h"
#include <stdio.h>

/* allocate global variables */
int lineno = 0;
FILE * source;
FILE * listing;
FILE * code;

/* allocate and set tracing flags */
int EchoSource = FALSE;
int TraceScan = FALSE;
int TraceParse = TRUE;
//int TraceAnalyze = FALSE;
//int TraceCode = FALSE;

int Error = FALSE;

void getsyntaxTree()
{ TreeNode * syntaxTree;
  source = fopen("SourceCode", "r");
  listing = fopen("Result", "w"); /* send listing to screen */
  fprintf(listing,"\nTINY COMPILATION:\n");
  syntaxTree = parse();
  if (TraceParse) {
    fprintf(listing,"\nSyntax tree:\n");
    printTree(syntaxTree);
  }
  fclose(source);
  fclose(listing);
}

