from decimal import *
import pdb
import sys, getopt

g_result = []
g_buckets = "N/A"
g_step = "N/A"
g_outfile = None
#g_sum = 1

def main():
  outName = "results.csv"
  opt, args = getopt.getopt(sys.argv[1:], "n:s:o:")
#  pdb.set_trace()
  try:
    for option, arg in opt:
      if option == '-n':
        global g_buckets
        g_buckets = int (arg)
      elif option == '-s':
        global g_step
        g_step = Decimal (arg)
      elif option == '-o':
        outName = arg + ".csv"
        print("Result will be saved to", outName)
      else:
        printUsage()
  except ValueError:
    printUsage()
    exit()
  
  if g_buckets == "N/A" or g_step == "N/A":
      printUsage()
      exit()
 
  if (validateInput() is not True):
    exit()
 
#  global g_sum
#  calcsum = int(log10(g_step))+1
#  g_step *= 10 ^ calcsum
#  g_sum *= 10 ^ calcsum
  try:  
    global g_outfile
    g_outfile = open(outName, "w")
    drawZL()
  
    saveFile()
    g_outfile.close()
  except KeyboardInterrupt:
    print("\nStopped")
    exit()
  except:
    if g_outfile is not None:
      g_outfile.close()
    print("\nFailed with unknown error.")
    raise
  print("\nCompleted")

def getBase():
  return [Decimal(0.0)] * g_buckets

def drawZL():
  leftsum = Decimal(1.0)
  pos = 0
#  pdb.set_trace()
  base = getBase()
  drawRest(base, leftsum, pos)

def drawRest(base, leftsum, pos):
  global g_result
  if leftsum == 0.0:
    g_result.append(base)
#    print("added %s", base)
    return

  res = base
  if pos == g_buckets:
   return 
  res[pos] = leftsum
  g_result.append(res[:])
  if (len(g_result) > 100):
    saveFile()
    sys.stdout.write(".")
    sys.stdout.flush()
    del g_result[:]
#  print("added %s", res)

  curleftsum = leftsum - g_step
  while (curleftsum >= 0):
    res[pos] = curleftsum
    drawRest(res, leftsum - curleftsum, pos + 1)
    curleftsum -= g_step

def validateInput():
  if g_buckets < 0:
    print("Number of buckets must >0. Given value=%s" % (g_buckets))
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

def printUsage():
  print("Usage:\n     %s [-n] number_of_buskets [-s] step_size [-o] output_file_name" % sys.argv[0])




main()
