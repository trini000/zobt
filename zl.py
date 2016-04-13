#!/usr/bin/env python

from decimal import *
import getopt, pdb, sys

g_result = []
g_baskets = "N/A"
g_step = "N/A"
g_outfile = None

def main():
  global g_baskets, g_step, g_outfile
  outName = "results.csv"
  opt, args = getopt.getopt(sys.argv[1:], "n:s:o:")
  try:
    for option, arg in opt:
      if option == '-n':
        g_baskets = int (arg)
      elif option == '-s':
        g_step = Decimal (arg)
      elif option == '-o':
        outName = arg + ".csv"
  except ValueError:
    printUsageAndExit()
  
  if g_baskets == "N/A" or g_step == "N/A":
      printUsageAndExit()
 
  if validateInput() is not True:
    exit()
 
  print("Calculating with baskets=%s and step=%s" % (g_baskets, g_step))
  print("Result will be saved to %s" % outName)
  try:  
    g_outfile = open(outName, "w")
    drawZL()
    saveFile()
    g_outfile.close()
  except KeyboardInterrupt:
    print("\nStopped")
    g_outfile.close()
    exit()
  except:
    g_outfile.close()
    print("\nFailed with unknown error.")
    raise
  print("\nCompleted")

def drawZL():
  leftsum = Decimal(1.0)
  pos = 0
  base = [Decimal(0.0)] * g_baskets
  drawRest(base, leftsum, pos)

def drawRest(base, leftsum, pos):
  global g_result
  if leftsum == 0.0:
    g_result.append(base)
#  print("added %s", base)
    return

  if pos == g_baskets:
    return
  base[pos] = leftsum
  g_result.append(base[:])
  if (len(g_result) > 100):
    saveFile()
    sys.stdout.write(".")
    sys.stdout.flush()
    del g_result[:]
#  print("added %s", base)

  curleftsum = leftsum - g_step
  while (curleftsum >= 0):
    base[pos] = curleftsum
    drawRest(base, leftsum - curleftsum, pos + 1)
    curleftsum -= g_step

def validateInput():
  if g_baskets < 0:
    print("Number of baskets must >0. Given value=%s" % (g_baskets))
    return False
  if g_step <= 0.0 or g_step >= 1.0:
    print("Step has to be in (0, 1). Given value=%s" % (g_step))
    return False
  step = float(g_step)
  while step < 1:
    step *= 10
  if 10 % step != 0:
    print("Fuck you! I don't calculate step=%s" % (g_step))
    return False
  return True

def saveFile():
  for row in g_result:
    g_outfile.write(', '.join(str(x) for x in row) + '\n')

def printUsageAndExit():
  print("Usage:\n     %s [-n] number_of_baskets [-s] step_size [-o] output_file_name" % sys.argv[0])
  exit()

main()
