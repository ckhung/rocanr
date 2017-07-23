//  Copyright 2013 Google Inc. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

// http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/
// https://stackoverflow.com/questions/27324292/convert-word2vec-bin-file-to-text
// modified by ckhung@cyut.edu.tw

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
#include <unistd.h>
#include <stdlib.h>

void print_help(char *argv[]);

int main(int argc, char *argv[]) {
  FILE *f;
  char const *file_name;
  float WW[500];	// word weights, max dim 500
  char vocab[300];	// an entry in the vocabulary, max length 300
  long nwi, nwo=-1, itr;// # of input words, # of output words, iterator
  int dim, k;
  char normalize=0;	// shall we normalize each vector?
  char ch, *chptr;

  while ((ch = getopt (argc, argv, "h1n:")) != -1)
    switch (ch) {
    case 'h':
      print_help(argv);
      return 0;
    case '1':
      normalize = 1;
      break;
    case 'n':
      nwo = strtol(optarg, &chptr, 10);
      break;
    default:
      fprintf(stderr, "unknown option -%c\n", optopt);
      print_help(argv);
      return -1;
    }

  if (argc <= optind) {
    print_help(argv);
    return -1;
  }
  file_name = argv[optind];
  f = fopen(file_name, "rb");
  if (f == NULL) {
    fprintf(stderr, "cannot open input file %s\n", file_name);
    return -1;
  }
  fscanf(f, "%ld", &nwi);
  fscanf(f, "%d", &dim);
  if (nwo < 0) {
    nwo = nwi;
  } else if (nwo > nwi) {
    fprintf(stderr, "warning: input has only %ld words\n", nwi);
    nwo = nwi;
  }
  printf("%ld %d\n", nwo, dim);
  for (itr = 0; itr < nwo; itr++) {
    fscanf(f, "%s%c", vocab, &ch);
    k = fread(WW, sizeof(float), dim, f);
    if (k < dim) {
	fprintf(stderr, "short read: %d < %d at %ld, ignore the rest\n",
	    k, dim, itr);
	break;
    }
    printf("%s ", vocab);
    if (normalize) {
      float len = 0;
      for (k = 0; k < dim; k++) len += WW[k] * WW[k];
      len = sqrt(len);
      for (k = 0; k < dim; k++) { WW[k] /= len; }
    }
    for (k = 0; k < dim-1; k++) { printf("%f ",WW[k]); }
    printf("%f\n", WW[dim-1]);
  }
  fclose(f);

  return 0;
}

void print_help(char *argv[]) {
  fprintf(stderr, "Usage: %s [-1] [-n N_OUT_WORDS] <FILE>\nwhere FILE contains word projections in google's binary format\n", argv[0]);
}

