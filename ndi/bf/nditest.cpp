#include <iostream>
#include <stdlib.h>

#include "data.h"
#include "item.h"
#include "ndi.h"

int main(int argc, char *argv[])
{
  NDI a;
  a.setData(argv[1]);
  a.setMinSup(std::atoi(argv[2]));
  a.setIEdepth(std::atoi(argv[3]));
  if(argc == 5) a.setOutputSets(argv[4]);
  int sets = a.generateSets();
  std::cout << sets << std::endl;
  return 0;
}
